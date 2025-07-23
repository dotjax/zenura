# suggestions

## sequence.py
1. sequence.py could be extended to support context windows (triplets, n-grams) for deeper modeling.

## daemon.py
1. Add error guards (e.g., corrupt file, import error, etc.) to daemon.py
2. Possible concurrency upgrade or throttling (e.g. asyncio, locks)
3. Allow plugin-like behavior or queue control

## bdx.py
1. Add a semantic layer atop bdx
2. Symbolic generalization (e.g., grouping, inference)
3. Natural language generation from sequence model
4. Memory pruning / reinforcement
5. Plug-in pipeline for new perception dimensions