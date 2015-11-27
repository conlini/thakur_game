Thakur's game of life

The game works on the principle of a special species that are not meant to discover each other. 
The world is divided into 2 species
* the "Thakur's". A species that is not permitted to disover others of its kind. 
* the "mazdoors". Normal inhabitants of the world


Rules
* The world is built of a 2D board M x N where M x N * 40.
* The game starts with the following players
	* There are 5% of Thakur's in the world randomly places based on the following rules
		1. 2 Thakur's can not be intially placed adjacent to each other(Diagnols do not count)
		2. 2 Thankurs can not be placed on the same cell
		3. 2 Thakur's shall not be intially placed in a single line with a single mazdoor in between(that is to say two Thakur's will not be seperated by a single mazdoor){Diagnols do not count}
	*  There will be 20% of mazdoors on the board randomly places and adhering to rule 3 above
* Each cell on the board will be assigned a Random direction(North/South/East/West).
* The game runs as follows
	* Each turn the inhabitants of the world move one step based on the direction as indicated by the block they occupy.
	* The world ends if any of the following happens
		1. 2 Thakur's land on the same cell
		2. 2 Thakur's land adjacent to each other(Diagnol do not count)
		3. 2 Thakur's are seperated/connected by a single mazdoor(Diagnol does not count)
	* If an edge cell has a direction pointing out the inhabitants enter from the opposite side(So a north cell pointing north, will cause the inhabitant to land up on the south edge)
	* Corners follow the same rule, except they land on the diagnolly opposite end
	* Every 20 iterations, the directions of the cells change

Objective: Develop a board with longest living inhabitants(max iterations)
