#include <stdio.h>
#include <stdlib.h>

void setup() {
  // put your setup code here, to run once:

  FILE *board;
  char buff[255];
  
  board = fopen( "../boards/10_14_success.board","r");

  fscanf(board, "%s", buff);
  printf("1 : %s\n", buff );
  
  
}

void loop() {
  // put your main code here, to run repeatedly:

}
