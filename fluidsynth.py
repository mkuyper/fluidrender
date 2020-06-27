from typing import cast, Any, Callable, List, Optional, Type, Union

import ctypes as ct
import ctypes.util as ctu
import inspect

class native:
    class utf8str(ct.c_char_p):
        @staticmethod
        def from_param(obj:Any) -> Any:
            if isinstance(obj, str):
                return obj.encode('utf-8')
            else:
                return ct.c_char_p.from_param(obj)

    def __init__(self, libname:str) -> None:
        lib = ctu.find_library(libname)
        if not lib:
            raise ValueError(f'Cannot find library {libname}')
        self.dll = ct.CDLL(lib)

    @staticmethod
    def argtype(f:Callable[...,Any], t:type, n:str) -> Optional[type]:
        if t is None:
            return None
        elif t is int:
            return ct.c_int
        elif t is str:
            return native.utf8str
        elif issubclass(t, inspect.getmro(ct.c_int)[1]):
            return t
        else:
            raise ValueError(f'{inspect.getsourcefile(f)}:{inspect.getsourcelines(f)[1]}: '
                    f'Missing type annotation for {n}')

    @staticmethod
    def paramtype(f:Callable[...,Any], p:inspect.Parameter) -> type:
        return cast(type, native.argtype(f, p.annotation, p.name))

    def __call__(self, f:Callable[...,Any]) -> Callable[...,Any]:
        sig = inspect.signature(f)
        pt = list([cast('Type[ct._CData]', native.paramtype(f, p))
            for p in sig.parameters.values()])
        rt = native.argtype(f, sig.return_annotation, 'return value')
        cf = ct.CFUNCTYPE(rt, *pt)
        return cf((f.__name__, self.dll))


class FluidSynth:
    @staticmethod
    @native('fluidsynth')
    def new_fluid_settings() -> ct.c_void_p: pass

    @staticmethod
    @native('fluidsynth')
    def delete_fluid_settings(settings:ct.c_void_p) -> None: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_settings_setstr(settings:ct.c_void_p, name:str, val:str) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_settings_setint(settings:ct.c_void_p, name:str, val:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def new_fluid_synth(settings:ct.c_void_p) -> ct.c_void_p: pass

    @staticmethod
    @native('fluidsynth')
    def delete_fluid_synth(synth:ct.c_void_p) -> None: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_synth_sfload(synth:ct.c_void_p, filename:str, reset_presets:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_synth_program_select(synth:ct.c_void_p, chan:int, sfont_id:int, bank_num:int, preset_num:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_synth_bank_select(synth:ct.c_void_p, chan:int, bank:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_synth_program_change(synth:ct.c_void_p, chan:int, prognum:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_synth_sfont_select(synth:ct.c_void_p, chan:int, sfont_id:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_synth_cc(synth:ct.c_void_p, chan:int, num:int, val:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def new_fluid_file_renderer(synth:ct.c_void_p) -> ct.c_void_p: pass

    @staticmethod
    @native('fluidsynth')
    def delete_fluid_file_renderer(dev:ct.c_void_p) -> None: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_file_renderer_process_block(dev:ct.c_void_p) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_synth_handle_midi_event(synth:ct.c_void_p, event:ct.c_void_p) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def new_fluid_midi_event() -> ct.c_void_p: pass

    @staticmethod
    @native('fluidsynth')
    def delete_fluid_midi_event(evt:ct.c_void_p) -> None: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_get_type(evt:ct.c_void_p) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_set_type(evt:ct.c_void_p, type:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_get_channel(evt:ct.c_void_p) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_set_channel(evt:ct.c_void_p, chan:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_get_key(evt:ct.c_void_p) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_set_key(evt:ct.c_void_p, key:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_get_velocity(evt:ct.c_void_p) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_set_velocity(evt:ct.c_void_p, vel:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_get_control(evt:ct.c_void_p) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_set_control(evt:ct.c_void_p, ctrl:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_get_value(evt:ct.c_void_p) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_set_value(evt:ct.c_void_p, val:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_get_program(evt:ct.c_void_p) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_set_program(evt:ct.c_void_p, val:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_get_pitch(evt:ct.c_void_p) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_midi_event_set_pitch(evt:ct.c_void_p, val:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def new_fluid_sequencer2(use_system_timer:int) -> ct.c_void_p: pass

    @staticmethod
    @native('fluidsynth')
    def delete_fluid_sequencer(seq:ct.c_void_p) -> None: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_sequencer_get_tick(seq:ct.c_void_p) -> ct.c_uint: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_sequencer_register_fluidsynth(seq:ct.c_void_p, synth:ct.c_void_p) -> ct.c_short: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_sequencer_send_at(seq:ct.c_void_p, evt:ct.c_void_p, time:ct.c_uint, absolute:int) -> int: pass

    @staticmethod
    @native('fluidsynth')
    def new_fluid_event() -> ct.c_void_p: pass

    @staticmethod
    @native('fluidsynth')
    def delete_fluid_event(evt:ct.c_void_p) -> None: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_event_get_source(evt:ct.c_void_p) -> ct.c_short: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_event_set_source(evt:ct.c_void_p, src:ct.c_short) -> None: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_event_get_dest(evt:ct.c_void_p) -> ct.c_short: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_event_set_dest(evt:ct.c_void_p, dest:ct.c_short) -> None: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_event_noteon(evt:ct.c_void_p, channel:int, key:ct.c_short, vel:ct.c_short) -> None: pass

    @staticmethod
    @native('fluidsynth')
    def fluid_event_pan(evt:ct.c_void_p, channel:int, val:ct.c_short) -> None: pass


class Settings:
    def __init__(self) -> None:
        self.pset = FluidSynth.new_fluid_settings()
        if not self.pset:
            raise MemoryError

    def __del__(self) -> None:
        FluidSynth.delete_fluid_settings(self.pset)

    def __setitem__(self, key:str, value:Union[int,str]) -> None:
        if isinstance(value, str):
            r = FluidSynth.fluid_settings_setstr(self.pset, key, value)
        elif isinstance(value, int):
            r = FluidSynth.fluid_settings_setint(self.pset, key, value)
        else:
            raise TypeError
        if r != 0:
            raise ValueError

class Synth:
    def __init__(self, settings:Settings) -> None:
        self.psynth = FluidSynth.new_fluid_synth(settings.pset)
        if not self.psynth:
            raise MemoryError
        self.pset = settings # prevent GC

    def __del__(self) -> None:
        FluidSynth.delete_fluid_synth(self.psynth)

    def sfload(self, fname:str, reset_presets:bool=True) -> int:
        r:int = FluidSynth.fluid_synth_sfload(self.psynth, fname,
                int(reset_presets))
        if r == -1:
            raise RuntimeError(f'Loading of soundfont "{fname}" failed.')
        return r

    def program_select(self, chan:int, sfid:int, bank:int, preset:int) -> None:
        r:int = FluidSynth.fluid_synth_program_select(self.psynth, chan, sfid, bank, preset)
        if r != 0:
            raise RuntimeError('Program selection failed.')

    def bank_select(self, chan:int, bank:int) -> None:
        r:int = FluidSynth.fluid_synth_bank_select(self.psynth, chan, bank)
        if r != 0:
            raise RuntimeError('Bank selection failed.')

    def sfont_select(self, chan:int, sfid:int) -> None:
        r:int = FluidSynth.fluid_synth_sfont_select(self.psynth, chan, sfid)
        if r != 0:
            raise RuntimeError('Soundfont selection failed.')

    def program_change(self, chan:int, program:int) -> None:
        r:int = FluidSynth.fluid_synth_program_change(self.psynth, chan, program)
        if r != 0:
            raise RuntimeError('Program change failed.')

    def cc(self, chan:int, num:int, val:int) -> None:
        r:int = FluidSynth.fluid_synth_cc(self.psynth, chan, num, val)
        if r != 0:
            raise RuntimeError('Controller event failed.')

class Sequencer:
    def __init__(self) -> None:
        self.pseq = FluidSynth.new_fluid_sequencer2(0)
        if not self.pseq:
            raise MemoryError
        self.synths:List[Synth] = []

    def __del__(self) -> None:
        FluidSynth.delete_fluid_sequencer(self.pseq)

    @property
    def tick(self) -> int:
        t:int = FluidSynth.fluid_sequencer_get_tick(self.pseq)
        return t

    def register_synth(self, synth:Synth) -> int:
        sid:int = FluidSynth.fluid_sequencer_register_fluidsynth(self.pseq, synth.psynth)
        self.synths.append(synth) # prevent GC
        return sid

    def send_at(self, evt:'Event', time:int, absolute:bool=True) -> None:
        r = FluidSynth.fluid_sequencer_send_at(self.pseq, evt.pevt, time, int(absolute))
        if r != 0:
            raise RuntimeError('Failed to schedule event.')


class Event:
    def __init__(self) -> None:
        self.pevt = FluidSynth.new_fluid_event()
        if not self.pevt:
            raise MemoryError

    def __del__(self) -> None:
        FluidSynth.delete_fluid_event(self.pevt)

    def noteon(self, channel:int, key:int, vel:int) -> None:
        FluidSynth.fluid_event_noteon(self.pevt, channel, key, vel)

    def pan(self, channel:int, value:int) -> None:
        FluidSynth.fluid_event_pan(self.pevt, channel, value)

    @property
    def source(self) -> int:
        return cast(int, FluidSynth.fluid_event_get_source(self.pevt))

    @source.setter
    def source(self, src:int) -> None:
        FluidSynth.fluid_event_set_source(self.pevt, src)

    @property
    def dest(self) -> int:
        return cast(int, FluidSynth.fluid_event_get_dest(self.pevt))

    @dest.setter
    def dest(self, src:int) -> None:
        FluidSynth.fluid_event_set_dest(self.pevt, src)


class FileRenderer:
    def __init__(self, synth:Synth) -> None:
        self.pdev = FluidSynth.new_fluid_file_renderer(synth.psynth)
        if not self.pdev:
            raise MemoryError
        self.synth = synth # prevent GC

    def __del__(self) -> None:
        FluidSynth.delete_fluid_file_renderer(self.pdev)

    def process_block(self) -> None:
        r = FluidSynth.fluid_file_renderer_process_block(self.pdev)
        if r != 0:
            raise RuntimeError('Failed to process block.')
