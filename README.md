# gamechain

This project is to test my hypothesis that the Bitcoin Cash (BCH) blockchain and mempool with zero-confirmation transaction times can make a good multi-player game lobby system.

You could signal your intent to start or join a game (or one of its variants) with a public key-based identity along with enough information to let participants connect/watch. Challengers could accept, and game moves/summaries/outcomes could published on the blockchain, too.

If you think of a game as a set of initial conditions and a series of validated transformations at the direction of participants (with some mechanism for randomness when appropriate), the game itself and how the players interact with it become two different applications. Game development consists of two components: client/user-interface and rules/validation engine. As long as you have a game and a complete specification of rules/protocols, gameplay can occur on-chain or off-chain (but still have moves be signed/authenticated by participants). Additionally, which clients people use become irrelevant to the game/blockchain itself as long as they validate according to the same sets of rules. Finally, games can resolve themselves the way they would off the blockchain - using observable behavior and conventions.

There are a lot of details to work out and conventions/protocols to support all types of games would be very important, but I am optimistic. One thing to note is that games that use randomness should be possible, but I'm starting as simply as possible. Many games have more than two players, which should also be possible, but I will start with only two players to keep communication simple while testing this hypothesis.


## Assumptions
This system works by using mempools and 0-conf to notify clients about transaction relevant to protocols used for game discovery and play. We will start with some basic assumptions.
* A Player is denoted by a BCH address. This BCH address is that Player's PlayerId.
* A Player uses their private key to sign/authenticate messages they transmit.
* A Player who wishes to start a game is called the Initiator.
* A Game is defined as: a set of initial conditions, rules that define valid actions players can take, how the game state changes based on those actions, transitions between Player turns, when the game ends, and what the outcome of the game is.
* A Game has a GameLobby identifier BCH address.  
* A Match is an instance of a Game. A concluded Match consists of initial conditions, at least one Player, and a series of Player-induced actions.

## Game Phases
This game lobby concept is broken up into two major phases. First, you must select a game, find the participants, and make sure everyone is clear on the rules/variant you are playing (initiating the game). Once that's done, gameplay can happen. How the game ends is ultimately up to the participants.

### Phase 1: Initiation
Sometimes harder than winning a game itself is finding, rounding up, and synchronizing players. Doing it digitally in an open platform is even worse. Let's see if we can't make it better with a flow something like that below. Note that this flow assumes a two-player game. Apart from message addresses (maybe use some type of group address), games with N-players should be able to flow in a similar fashion.

#### Message: Looking for Game (LFG)
We need a way for the Initiator to broadcast a signal that they would like to start a game. To do this, the Initiator sends a specially constructed _Looking for Game_ transaction to the GameLobby address of the Game they want to start. The transaction contains the following information in the OP_RETURN:
* Looking for Group message code
* Group Id (unique to Initiator)
* Proposed Initial Condition Data
* Game Participant Requirements

Due to the nature of BCH transactions, the message will include the Initiator's PlayerId.

#### Message: Willing to Play (WTP)
Anyone listening to a GameLobby address will see LFG transactions for that Game. If they are interested in playing, they will send a transaction to the Initiator's PlayerId. The transaction contains the following information in the OP_RETURN:
* I Challenge message code
* the transaction ID of the LFG transaction being responded to
* (optional) Required Mods to Initial Condition Data

Additionally, the message will include the Responder's PlayerId due to the nature of BCH transactions.

#### Message: Accept/Reject
Once the Initiator has received responses, it's polite to accept or deny the Responder and start the game. This is done by the Initiator sending a message to the Responder's PlayerId. 

To turn down the challenge, the transaction contains the following information in the OP_RETURN:
* I Reject message code
* the transaction ID of the WTP transaction being responded to

To accept the challenge, the transaction contains the following information in the OP_RETURN:
* I Accept message code
* the transaction ID of the WTP transaction being responded to
* a Match Id (for two players, the WTP transaction ID is sufficient)
* Initial Condition Data

The message that contains the Match Id and Initial Condition Data is the first step of the Match.

### Phase 2: Play
This is driven by the Game being played. These are some common interactions which should be common to most (if not all) games. The important things to publish on-chain so that they can be seen/recorded/agreed as fair are: game decisions during a turn, assessed outcomes of those game decisions, turn hand-off between players, resolving the game (win/loss/draw)and being able to disagree about the outcome (e.g. bug in rules, invalid play, flip the table, etc.). 

While games might be able to be encoded as Script, I think it's more important to enable games without requiring a centralized protocol (which means they could be... they just don't *have* to be). Admittedly this is hand-waving at this point. Coming up with a game initialization/play mechanism and implementing a range of games to do that in a range of use cases is the point of this project. 

 #### Message/Action: Take My Turn
 The transaction contains the following information in the OP_RETURN:
 * Take My Turn message code
 * turn operations (game-specific)
 * previous Match step transaction ID
 
 #### Message/Action: It's Over
 The transaction contains the following information in the OP_RETURN:
 * It's Over message code (I Win, I Lose, We Tie, I Concede)
 * turn operations (game-specific)
 * previous Match step transaction ID
 
 #### Message/Action: I Acknowledge Outcome
 The transaction contains the following information in the OP_RETURN:
 * I Acknowledge Outcome message code
 * acknowledgement message (free form)
 * previous Match step transaction ID
 
 #### Message/Action: I Dispute
 The transaction contains the following information in the OP_RETURN:
 * I Dispute message code
 * dispute explanation (free form; the relevance of this is ultimately determined by how much participants and public/historical observers cares)
 * previous Match step transaction ID
 
 
 