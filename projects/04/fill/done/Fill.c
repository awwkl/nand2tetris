// pseudocode
// int currentPixel = SCREEN

// while (true) {
//   check if keyPressed;

//   if (keyPressed) {
//     *currentPixel = -1;    // set it to black (1111 1111 1111 1111)
//     if (currentPixel == 24575) {
//       break;
//     }
//     currentPixel++;
//   }
//   else {
//     *currentPixel = 0;     // set it to white (0000 0000 0000 0000)
//     if (currentPixel == SCREEN) {
//       break;
//     }
//     currentPixel--;
//   }
// }