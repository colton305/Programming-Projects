
//Jacks or Better Video Poker

//Starting with 10 coins, try to last as many turns as possible
//In the top right corner, it tells you what hand you have
//The hands pay as follows:
//Straight Flush: 50 coins
//Four of a Kind: 25 coins
//Full House: 9 coins
//Flush: 6 coins
//Straight: 4 coins
//Three of a Kind: 3 coins
//Two Pairs: 2 coins
//High Pair(Jacks or Better): 1 coin
//Low Pair: 0 coins

//Controls:
//Press P to draw 5 cards
//Once the 5 cards are dealt, click on a card to hold it, and once you are satisfied with your choices press P again

String[][] deck = new String[13][4];
String[] suits = {" of Spades", " of Hearts", " of Diamonds", " of Clubs"};
int[] cardNum = new int[5];
int[] cardSuit = new int[5];
boolean straight = false;
boolean flush = false;
int pairNum = 0;
boolean frames = false;
boolean[] cardSelected = new boolean[5];
boolean redraw = false;
boolean highPair = false;
int coins = 10;
int turnsLasted = 0;
boolean notBroke = true;

void setup() {
  size(1000,500);
  background(#64C832);
  for(int i = 0; i < deck.length; i++) {
    for(int j = 0; j < deck[i].length; j++) {
      if(i == 0) {
        deck[i][j] = ("Ace") + suits[j];
      }
      else if(i == 10) {
        deck[i][j] = ("Jack") + suits[j]; 
      }
      else if(i == 11) {
        deck[i][j] = ("Queen") + suits[j]; 
      }
      else if(i == 12) {
        deck[i][j] = ("King") + suits[j]; 
      }
      else {
        deck[i][j] = (i+1) + suits[j]; 
      }
      println(deck[i][j]);
    }
  }
}

void draw() {
  if(coins < 1) {
    notBroke = false; 
  }
  if(notBroke == true) {
  textSize(20);
  text("Coins: "+coins,25,25);
  text("Turns Lasted: "+turnsLasted,25,50);
  }
  else {
    background(#64C832);
    textSize(100);
    text("Game Over",250,250);
    textSize(40);
    text("Turns Lasted: "+turnsLasted,250,350);
  }
}

void mousePressed() {
  for(int p=200;p<=1000;p+=200) {
    if((p-150<mouseX&&mouseX<p-50)&&(150<mouseY&&mouseY<350)) {
      if(cardSelected[p/200-1] == false) {
        stroke(#FFFF00);
        strokeWeight(4);
        line(p-150,150,p-50,150);
        line(p-50,150,p-50,350);
        line(p-150,350,p-50,350);
        line(p-150,150,p-150,350);
        cardSelected[p/200-1] = true;
      }
      else {
        stroke(#64C832);
        strokeWeight(4);
        line(p-150,150,p-50,150);
        line(p-50,150,p-50,350);
        line(p-150,350,p-50,350);
        line(p-150,150,p-150,350);
        stroke(#000000);
        strokeWeight(1);
        line(p-150,150,p-50,150);
        line(p-50,150,p-50,350);
        line(p-150,350,p-50,350);
        line(p-150,150,p-150,350);
        cardSelected[p/200-1] = false;
      }
    }
  }
}

void keyPressed() {
  
  if(key == 's') {
    for (int i = 12; i>1; i--){
      for (int j = 3; j>1; j--) {
        int randomIndex = int(random(12));
        int randomIndexNum = int(random(3));
        String temp = deck[i][j];
        deck[i][j] = deck[randomIndex][randomIndexNum];
        deck[randomIndex][randomIndexNum] = temp;
        println(deck[i][j]);
      }
    }
  }
  
  if(key == 'p') {
    if(redraw == true) {
      for(int s=200;s<=1000;s+=200) {
        if(cardSelected[s/200-1] == false) {
          fill(#FFFFFF);
          stroke(#000000);
          strokeWeight(1);
          rect(s-150,150,100,200);
          textMode(CENTER);
          textSize(100);
          if(deck[s/200+4][0].indexOf("Spade") >= 0) {
            cardSuit[s/200-1] = 1;
            fill(#000000);
          }
          if(deck[s/200+4][0].indexOf("Heart") >= 0) {
            cardSuit[s/200-1] = 2;
            fill(#FF0000);
          }
          if(deck[s/200+4][0].indexOf("Diamond") >= 0) {
            cardSuit[s/200-1] = 3;
            fill(#0000FF);
          }
          if(deck[s/200+4][0].indexOf("Club") >= 0) {
            cardSuit[s/200-1] = 4;
            fill(#00FF00);
          }
          if(deck[s/200+4][0].indexOf("Ace") >= 0) {
            text("A", s-133,280);
            cardNum[s/200-1] = 1;
          }
          if(deck[s/200+4][0].indexOf("2") >= 0) {
            text("2", s-133,280);
            cardNum[s/200-1] = 2;
          }
          if(deck[s/200+4][0].indexOf("3") >= 0) {
            text("3", s-133,280);
            cardNum[s/200-1] = 3;
          }
          if(deck[s/200+4][0].indexOf("4") >= 0) {
            text("4", s-133,280);
            cardNum[s/200-1] = 4;
          }
          if(deck[s/200+4][0].indexOf("5") >= 0) {
            text("5", s-133,280);
            cardNum[s/200-1] = 5;
          }
          if(deck[s/200+4][0].indexOf("6") >= 0) {
            text("6", s-133,280);
            cardNum[s/200-1] = 6;
          }
          if(deck[s/200+4][0].indexOf("7") >= 0) {
            text("7", s-133,280);
            cardNum[s/200-1] = 7;
          }
          if(deck[s/200+4][0].indexOf("8") >= 0) {
            text("8", s-133,280);
            cardNum[s/200-1] = 8;
          }
          if(deck[s/200+4][0].indexOf("9") >= 0) {
            text("9", s-133,280);
            cardNum[s/200-1] = 9;
          }
          if(deck[s/200+4][0].indexOf("10") >= 0) {
            textSize(80);
            text("10", s-153,280);
            cardNum[s/200-1] = 10;
          }
          if(deck[s/200+4][0].indexOf("Jack") >= 0) {
            text("J", s-113,280);
            cardNum[s/200-1] = 11;
          }
          if(deck[s/200+4][0].indexOf("Queen") >= 0) {
            text("Q", s-133,280);
            cardNum[s/200-1] = 12;
          }
          if(deck[s/200+4][0].indexOf("King") >= 0) {
            text("K", s-133,280);
            cardNum[s/200-1] = 13;
          }
        }
      }
      redraw = false;
      straight = false;
      flush = false;
      pairNum = 0;
    }
    else {
    coins--;
    redraw = true;
    straight = false;
    flush = false;
    pairNum = 0;
    for(int l=0;l<52;l++) {
    for (int k = 12; k>1; k--){
      for (int j = 3; j>1; j--) {
        int randomIndex = int(random(12));
        int randomIndexNum = int(random(3));
        String temp = deck[k][j];
        deck[k][j] = deck[randomIndex][randomIndexNum];
        deck[randomIndex][randomIndexNum] = temp;
      }
    }
    background(#64C832);
    for(int r=0;r<5;r++) {
      cardSelected[r] = false;
    }
    for(int i=200;i<=1000;i+=200) {
      fill(#FFFFFF);
      stroke(#000000);
      strokeWeight(1);
      rect(i-150,150,100,200);
      textMode(CENTER);
      textSize(100);
    if(deck[i/200-1][0].indexOf("Ace") >= 0) {
      if(deck[i/200-1][0].indexOf("Spade") >= 0) {
        fill(#000000);
      }
      if(deck[i/200-1][0].indexOf("Heart") >= 0) {
        fill(#FF0000);
      }
      if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
        fill(#0000FF);
      }
      if(deck[i/200-1][0].indexOf("Club") >= 0) {
        fill(#00FF00);
      }
        text("A", i-133,280);
        cardNum[i/200-1] = 1;
      }
    if(deck[i/200-1][0].indexOf("2") >= 0) {
       if(deck[i/200-1][0].indexOf("Spade") >= 0) {
        fill(#000000);
      }
      if(deck[i/200-1][0].indexOf("Heart") >= 0) {
        fill(#FF0000);
      }
      if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
        fill(#0000FF);
      }
      if(deck[i/200-1][0].indexOf("Club") >= 0) {
        fill(#00FF00);
      }
      text("2", i-133,280);
      cardNum[i/200-1] = 2;
    }
    if(deck[i/200-1][0].indexOf("3") >= 0) {
       if(deck[i/200-1][0].indexOf("Spade") >= 0) {
        fill(#000000);
      }
      if(deck[i/200-1][0].indexOf("Heart") >= 0) {
        fill(#FF0000);
      }
      if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
        fill(#0000FF);
      }
      if(deck[i/200-1][0].indexOf("Club") >= 0) {
        fill(#00FF00);
      }
      text("3", i-133,280);
      cardNum[i/200-1] = 3;
    }
    if(deck[i/200-1][0].indexOf("4") >= 0) {
       if(deck[i/200-1][0].indexOf("Spade") >= 0) {
        fill(#000000);
        cardSuit[i/200-1] = 1;
      }
      if(deck[i/200-1][0].indexOf("Heart") >= 0) {
        fill(#FF0000);
      }
      if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
        fill(#0000FF);
      }
      if(deck[i/200-1][0].indexOf("Club") >= 0) {
        fill(#00FF00);
      }
      text("4", i-133,280);
      cardNum[i/200-1] = 4;
    }
    if(deck[i/200-1][0].indexOf("5") >= 0) {
       if(deck[i/200-1][0].indexOf("Spade") >= 0) {
        fill(#000000);
      }
      if(deck[i/200-1][0].indexOf("Heart") >= 0) {
        fill(#FF0000);
      }
      if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
        fill(#0000FF);
      }
      if(deck[i/200-1][0].indexOf("Club") >= 0) {
        fill(#00FF00);
      }
      text("5", i-133,280);
      cardNum[i/200-1] = 5;
    }
    if(deck[i/200-1][0].indexOf("6") >= 0) {
       if(deck[i/200-1][0].indexOf("Spade") >= 0) {
        fill(#000000);
      }
      if(deck[i/200-1][0].indexOf("Heart") >= 0) {
        fill(#FF0000);
      }
      if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
        fill(#0000FF);
      }
      if(deck[i/200-1][0].indexOf("Club") >= 0) {
        fill(#00FF00);
      }
      text("6", i-133,280);
      cardNum[i/200-1] = 6;
    }
    if(deck[i/200-1][0].indexOf("7") >= 0) {
       if(deck[i/200-1][0].indexOf("Spade") >= 0) {
        fill(#000000);
      }
      if(deck[i/200-1][0].indexOf("Heart") >= 0) {
        fill(#FF0000);
      }
      if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
        fill(#0000FF);
      }
      if(deck[i/200-1][0].indexOf("Club") >= 0) {
        fill(#00FF00);
      }
      text("7", i-133,280);
      cardNum[i/200-1] = 7;
    }
    if(deck[i/200-1][0].indexOf("8") >= 0) {
       if(deck[i/200-1][0].indexOf("Spade") >= 0) {
        fill(#000000);
      }
      if(deck[i/200-1][0].indexOf("Heart") >= 0) {
        fill(#FF0000);
      }
      if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
        fill(#0000FF);
      }
      if(deck[i/200-1][0].indexOf("Club") >= 0) {
        fill(#00FF00);
      }
      text("8", i-133,280);
      cardNum[i/200-1] = 8;
    }
    if(deck[i/200-1][0].indexOf("9") >= 0) {
       if(deck[i/200-1][0].indexOf("Spade") >= 0) {
        fill(#000000);
      }
      if(deck[i/200-1][0].indexOf("Heart") >= 0) {
        fill(#FF0000);
      }
      if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
        fill(#0000FF);
      }
      if(deck[i/200-1][0].indexOf("Club") >= 0) {
        fill(#00FF00);
      }
      text("9", i-133,280);
      cardNum[i/200-1] = 9;
    }
    if(deck[i/200-1][0].indexOf("10") >= 0) {
       if(deck[i/200-1][0].indexOf("Spade") >= 0) {
        fill(#000000);
      }
      if(deck[i/200-1][0].indexOf("Heart") >= 0) {
        fill(#FF0000);
      }
      if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
        fill(#0000FF);
      }
      if(deck[i/200-1][0].indexOf("Club") >= 0) {
        fill(#00FF00);
      }
      textSize(80);
      text("10", i-153,280);
      cardNum[i/200-1] = 10;
    }
    if(deck[i/200-1][0].indexOf("Jack") >= 0) {
       if(deck[i/200-1][0].indexOf("Spade") >= 0) {
        fill(#000000);
      }
      if(deck[i/200-1][0].indexOf("Heart") >= 0) {
        fill(#FF0000);
      }
      if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
        fill(#0000FF);
      }
      if(deck[i/200-1][0].indexOf("Club") >= 0) {
        fill(#00FF00);
      }
      text("J", i-113,280);
      cardNum[i/200-1] = 11;
    }
    if(deck[i/200-1][0].indexOf("Queen") >= 0) {
       if(deck[i/200-1][0].indexOf("Spade") >= 0) {
        fill(#000000);
      }
      if(deck[i/200-1][0].indexOf("Heart") >= 0) {
        fill(#FF0000);
      }
      if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
        fill(#0000FF);
      }
      if(deck[i/200-1][0].indexOf("Club") >= 0) {
        fill(#00FF00);
      }
      text("Q", i-133,280);
      cardNum[i/200-1] = 12;
    }
    if(deck[i/200-1][0].indexOf("King") >= 0) {
       if(deck[i/200-1][0].indexOf("Spade") >= 0) {
        fill(#000000);
      }
      if(deck[i/200-1][0].indexOf("Heart") >= 0) {
        fill(#FF0000);
      }
      if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
        fill(#0000FF);
      }
      if(deck[i/200-1][0].indexOf("Club") >= 0) {
        fill(#00FF00);
      }
      text("K", i-133,280);
      cardNum[i/200-1] = 13;
    }
    if(deck[i/200-1][0].indexOf("Spade") >= 0) {
      cardSuit[i/200-1] = 1;
    }
    if(deck[i/200-1][0].indexOf("Heart") >= 0) {
      cardSuit[i/200-1] = 2;
    }
    if(deck[i/200-1][0].indexOf("Diamond") >= 0) {
      cardSuit[i/200-1] = 3;
    }
    if(deck[i/200-1][0].indexOf("Club") >= 0) {
      cardSuit[i/200-1] = 4;
    }
    print(cardNum[i/200-1]);
    println(cardSuit[i/200-1]);
    }
    }
    }
    for(int m=0;m<5;m++) {
      for(int mi=0;mi<5;mi++) {
        for(int mii=0;mii<5;mii++) {
          for(int miii=0;miii<5;miii++) {
            for(int miiii=0;miiii<5;miiii++) {
              if(cardNum[m]-1 == cardNum[mi] && cardNum[mi]-1 == cardNum[mii] && cardNum[mii]-1 == cardNum[miii] && cardNum[miii]-1 == cardNum[miiii]) {
                straight = true;
              }
            }
          }
        }
      }
    }
    if(cardSuit[0] == cardSuit[1] && cardSuit[1] == cardSuit[2] && cardSuit[2] == cardSuit[3] && cardSuit[3] == cardSuit[4]) {
      flush = true;
    }
    for(int n=0;n<5;n++) {
      for(int o=0;o<5;o++) {
        if(n != o) {
          if(cardNum[n] == cardNum[o]) {
            pairNum++;
            if(cardNum[n] > 10 || cardNum[n] == 1) {
              highPair = true;
            }
            else {
              highPair = false; 
            }
          }
        }
      }
    }
    //Actual hand checker
    fill(#64C832);
    stroke(#64C832);
    rect(0,0,1000,50);
    textSize(20);
    fill(#FFFFFF);
    if(redraw == true) {
    if(straight == true && flush == true) {
      text("Straight-Flush!",750,25);
    }
    else if(pairNum == 12) {
      text("Four of a Kind!",750,25); 
    }
    else if(pairNum == 8) {
      text("Full House!",750,25); 
    }
    else if(flush == true) {
      text("Flush!",750,25); 
    }
    else if(straight == true) {
      text("Straight!",750,25); 
    }
    else if(pairNum == 6) {
      text("Three of a Kind!",750,25); 
    }
    else if(pairNum == 4) {
      text("Two Pairs!",750,25); 
    }
    else if(pairNum == 2 && highPair == true) {
      text("High Pair!",750,25); 
    }
    else if(pairNum == 2 && highPair == false) {
      text("Low Pair",750,25);
    }
    else {
      text("Nothing :/",750,25); 
    }
    }
    else {
      if(straight == true && flush == true) {
      text("Straight-Flush!",750,25);
      textSize(60);
      text("Winner!",250,100);
      coins += 50;
    }
    else if(pairNum == 12) {
      text("Four of a Kind!",750,25); 
      textSize(60);
      text("Winner!",250,100);
      coins += 25;
    }
    else if(pairNum == 8) {
      text("Full House!",750,25); 
      textSize(60);
      text("Winner!",250,100);
      coins += 9;
    }
    else if(flush == true) {
      text("Flush!",750,25); 
      textSize(60);
      text("Winner!",250,100);
      coins += 6;
    }
    else if(straight == true) {
      text("Straight!",750,25); 
      textSize(60);
      text("Winner!",250,100);
      coins += 4;
    }
    else if(pairNum == 6) {
      text("Three of a Kind!",750,25); 
      textSize(60);
      text("Winner!",250,100);
      coins += 3;
    }
    else if(pairNum == 4) {
      text("Two Pairs!",750,25); 
      textSize(60);
      text("Winner!",250,100);
      coins += 2;
    }
    else if(pairNum == 2 && highPair == true) {
      text("High Pair!",750,25); 
      textSize(60);
      text("Winner!",250,100);
      coins += 1;
    }
    else if(pairNum == 2 && highPair == false) {
      text("Low Pair",750,25);
      textSize(60);
      text("Loser :(",250,100);
    }
    else {
      text("Nothing :/",750,25); 
      textSize(60);
      text("Loser :(",250,100);
    }
    turnsLasted++;
    }
  }
}
