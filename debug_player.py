import importlib, sys
sys.path.insert(0, r'C:\Users\Maxmoney\Documents\pygame.rougelike.surv')
mod = importlib.import_module('Player')
print('SCREEN_WIDTH in module:', hasattr(mod, 'SCREEN_WIDTH'))
print('SCREEN_WIDTH value:', getattr(mod, 'SCREEN_WIDTH', None))
print('module file:', getattr(mod, '__file__', None))
print('Player class present:', hasattr(mod, 'Player'))
print('Player.update source lines around clamp:')
import inspect
print('\n'.join(inspect.getsource(mod).splitlines()[60:100]))
