import sys
import asyncio

from phase1 import phase1
from phase2 import phase2


if __name__ == '__main__':
    try:
        phase = sys.argv[1].lower()
        
        if phase == 'phase1':
            print("Running phase 1...")
            loop = asyncio.get_event_loop()
            sys.exit(loop.run_until_complete(phase1.main()))
        elif phase == 'phase2':
            print("Running phase 2...")
            sys.exit(phase2.main())
        else:
            raise ValueError("error: invalid phase")
        
    except IndexError:
        print('Usage: python3 mini-project2 phase[1-2]')
        sys.exit(1)

    except ValueError as e:
        print(e)
        sys.exit(1)

        
    
