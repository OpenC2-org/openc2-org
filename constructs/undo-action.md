## Construct

### Proposed

Add Universal UNDO action to reverse any previously issued command

|||
| :--- | :--- |
| **Affirmative Construct** |  **Negative Construct** | 
| - Convenient means to cancel an action <br>- Due diligence requires ability to recover from an action to a known good state | - Requires significant level of state to be maintained <br>- Not scalable/ implementable for inter-domain C2 <br>- Commands are appended as contextual information is acquired tracking all commands complex <br>- Not applicable to many actions |
| **Negative Rebuttal** | **Affirmative Rebuttal** |
| - The lack of applicability for some commands (such as DETONATE) does not invalidate UNDO for all commands <br>- A network defense system should maintain state anyway, so the UNDO command should not be an undue burden | - Potentially complex undo procedures, thus NOT convenient means to cancel actions <br>- The lack of the UNDO command does not preclude the implementation of recovery, simply does not require explicit action <br>- Not actually universal: UNDO/STOP, UNDO/DETONATE <br>- Specific “undo-like” OpenC2 actions already defined |

### Resolution

Returning to known good states and maintenance of history is left to the implementer and a universal UNDO should not be included in the command set.

### Minority Report

A universal UNDO command should be included so that implementers have a convenient means to return to a known good state.
