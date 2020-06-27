#!/usr/bin/env python3

from typing import Any, Dict, List, Tuple

import click
import mido
import os
import tempfile
import warnings
import yaml

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pydub

from fluidsynth import Event, FileRenderer, Sequencer, Settings, Synth

def find_file(filename:str, dirs:List[str]) -> str:
    if not os.path.isabs(filename) and not os.path.isfile(filename):
        for d in dirs:
            cfn = os.path.join(d, filename)
            if os.path.isfile(cfn):
                return cfn
    return filename

def render_track(track:mido.MidiFile, filename:str, soundfont:str, instrument:Dict[str,Any]) -> None:
    settings = Settings()
    settings['audio.file.name'] = filename
    settings['player.timing-source'] = 'sample'
    settings['synth.lock-memory'] = 0

    synth = Synth(settings)
    sfid = synth.sfload(soundfont, reset_presets=False)

    seq = Sequencer()
    seqid = seq.register_synth(synth)

    evt = Event()
    evt.source = -1
    evt.dest = seqid

    renderer = FileRenderer(synth)

    synth.program_select(0, sfid, instrument['bank'], instrument['preset'])

    time = 1.0
    tsp = instrument.get('tsp', 0)

    for msg in track:
        time += msg.time
        if msg.type == 'note_on':
            evt.noteon(0, msg.note+tsp, msg.velocity)
            seq.send_at(evt, round(time * 1000))

    tend = round((time + 1.0) * 1000)
    while seq.tick < tend:
        renderer.process_block()

@click.command()
@click.argument('mapfile', type=click.Path(exists=True))
@click.argument('midifile', type=click.Path(exists=True))
@click.argument('outfile', type=click.Path())
def render(mapfile:str, midifile:str, outfile:str) -> None:
    with open(mapfile) as fh:
        info = yaml.safe_load(fh)


    soundfont = find_file(info['soundfont'], [
        os.path.dirname(os.path.realpath(mapfile)), # search mapfile directory
        os.path.dirname(os.path.realpath(__file__)),# search script directory
        ])

    mf = mido.MidiFile(midifile)

    trackno = 0
    audiofiles:List[Tuple[str,Dict[str,Any]]] = list()

    ctrack = mf.tracks.pop(0)

    with tempfile.TemporaryDirectory() as tmpdir:
        for track in mf.tracks:
            if (instruments := info['instruments'].get(track.name)) is None:
                print(f'skipping unmapped track {track.name}')
                continue

            trackmf = mido.MidiFile(ticks_per_beat=mf.ticks_per_beat)
            trackmf.tracks = [ctrack, track]
            for instrument in instruments:
                fn = f'{tmpdir}/{trackno}.wav'
                render_track(trackmf, f'{tmpdir}/{trackno}.wav', soundfont, instrument)
                audiofiles.append((fn, instrument))
                trackno += 1

        segments:List[pydub.AudioSegment] = list()
        maxlen = 0
        for fn, instrument in audiofiles:
            seg = pydub.AudioSegment.from_file(fn, format='wav')
            if (gain := instrument.get('gain', 0.0)):
                seg = seg + gain
            if (pan := instrument.get('pan', 0.0)):
                seg = seg.pan(pan)
            if (l := len(seg)) > maxlen:
                maxlen = l
            segments.append(seg)

        audio = pydub.AudioSegment.silent(duration=maxlen)
        for segment in segments:
            audio = audio.overlay(segment)

        audio.export(outfile, format='wav')

if __name__ == '__main__':
    render()
