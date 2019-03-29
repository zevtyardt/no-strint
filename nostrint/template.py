# <-- TEMPLATE -->

# {0} -> 0
# {1} -> strint
ZERO_BASE = ['( ( lambda : {0} ) . func_code . co_lnotab ) . join ( map ( chr , [ {1} ] ) )',
             '( lambda _ : _ ( map ( chr , [ {1} ] ) ) ) ( ( ( lambda : {0} ) . func_code . co_lnotab ) . join )',
             'str ( bytearray ( ( {1} , ) ) )']
# {0} -> 256
# {1} -> 0
# {2} -> strint
ENCODE_BASE = ['( lambda _ , __ : _ ( _ , __ ) ) ( lambda _ , __ : chr ( __ % {0} ) + _ ( _ , __ // {0} ) if __ else ( ( lambda : {1} ) . func_code . co_lnotab ) , {2} )']

# {0} -> 1    {3} -> 8
# {1} -> 2    {4} -> ZERO_BASE
# {2} -> 5
STDOUT_BASE = ['getattr ( __import__ ( True . __class__ . __name__ [ {0} ] + [ ] . __class__ . __name__ [ {1} ] ) , ( ) . __class__ . __eq__ . __class__ . __name__ [ : {1} ] + ( ) . __iter__ ( ) . __class__ . __name__ [ {2} : {3} ] ) ( {0}, {4} + chr ( {2} + {2} ) )']

# {0} -> '<string>'   {3} -> 95
# {1} -> 'exec'       {4} -> strint
# {2} -> 1            {5} -> 0
EXEC_BASE = ['( lambda __ : [ ( eval ( compile ( _ , {0} , {1} ) , None , __ ) , None ) [ {2} ] for __ [ chr ( {3} ) ] in [ ( {4} ) ] ] [ {5} ] ) ( globals ( ) )']

# ''
NULL_STR = ['( ( lambda : {0} ) . func_code . co_lnotab )',
            'str ( )']
