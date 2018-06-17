# gamechain
This project is to test my hypothesis that the Bitcoin Cash (BCH) blockchain and mempool with zero-confirmation transaction times can make a reasonable, open, non-proprietary game event system for non-realtime multi-player game participation.

It is a companion protocol to [GameChain Lobby](https://github.com/devalbo/gamechain-lobby).

### What is a Game?
If you think of a game as a set of initial conditions and a series of validated transformations at the direction of participants (with some mechanism for randomness when appropriate), the game itself and how the players interact with it become two different applications. Game development consists of two components: client/user-interface and rules/validation engine. As long as you have a game and a complete specification of rules/protocols, gameplay can occur on-chain or off-chain (but still have moves be signed/authenticated by participants). Additionally, which clients people use become irrelevant to the game/blockchain itself as long as they validate according to the same sets of rules. Finally, games can resolve themselves the way they would off the blockchain - using observable behavior and conventions.

## Scope
Typical games involve players taking turns making decisions. In theory, this back and forth can occur in messages encoded as blockchain transactions. With the proper abstraction, most classic games could be codified this way. 

### There's a lot to do yet...
There are a lot of details to work out and conventions/protocols to support all types of games would be very important, but I am optimistic. One thing to note is that games that use randomness should be possible, but I'm starting as simply as possible. Many games have more than two players, which should also be possible, but I will start with only two players to keep communication simple while testing this hypothesis.

## Assumptions
This system works by using mempools and 0-conf to notify clients about transaction relevant to protocols used for game discovery and play. We will start with some basic assumptions.
* A Player is denoted by a BCH address. This BCH address is that Player's PlayerId.
* A Player uses their private key to sign/authenticate messages they transmit.
* A Player who wishes to start a game is called the Initiator.
* A Game is defined as: a set of initial conditions, rules that define valid actions players can take, how the game state changes based on those actions, transitions between Player turns, when the game ends, and what the outcome of the game is.
* A Game has a GameLobby identifier BCH address.  
* A Match is an instance of a Game. A concluded Match consists of initial conditions, at least one Player, and a series of Player-induced actions.

## Protocol Messages
The use of this protocol is driven by the Game being played. These are some common interactions which should be common to most (if not all) games. The important things to publish on-chain so that they can be seen/recorded/agreed as fair are: game decisions during a turn, assessed outcomes of those game decisions, turn hand-off between players, resolving the game (win/loss/draw)and being able to disagree about the outcome (e.g. bug in rules, invalid play, flip the table, etc.). 

While games might be able to be encoded as Script, I think it's more important to enable games without requiring a centralized protocol (which means they could be Script-based... they just don't *have* to be). Admittedly this is hand-waving at this point. Coming up with a game initialization/play mechanism and implementing a range of games to do that in a range of use cases is the point of this project. 

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
 
 
 