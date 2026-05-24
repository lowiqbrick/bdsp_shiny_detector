# Pokémon FireRed shiny detection

## Description

Pokémon FireRed and LeafGreen were added to the library of the switch 2 on [february 28th](https://www.nintendo.com/au/news-and-articles/pokemon-firered-version-and-pokemon-leafgreen-version-are-coming-to-nintendo/?srsltid=AfmBOooBnTxjd0p7R1-ArnCzsWDhgsDODFkLUY3nNJLHx3Kkty5d2hZR).

In these games it is possible to catch shiny Pokémon. These are rare instances of Pokémon which posses different colors than regular Pokémon. Think of them as the Pokémon equivalent of albinos in the animal world. They don't learn different or stronger moves than regular Pokémon. It's just bragging rights. Obtaining them requires either luck of lots of hours to find one.

With a third party video game controller that has macros build in, it is possible to hunt for shiny Pokémon. That is because there are instances of legendary Pokémon encounters that are stationary, since a Pokémon being shiny is always rolled the moment a battle begins. So a macro can be run to automatically start battles and reset the game over and over again. One such cycle takes approximately 20 seconds. With the odds of a Pokémon being shiny being to 1/8192, one can expect to encounter a shiny Pokémon approximately every 45.5 hours. A controller can take care of that with a macro, saving someone from having to do that oneself. 

The issue with this approach is that the controller does that forever, even if a shiny Pokémon actually shows up.

This requires something to turn the controller of once a shiny encounter is present. This is where this repository comes in.

## Controller Macro

![image](readme_images/controller_macro.png)

The macro used in this project is shown in the image above. The image is taken from the controllers configuration software [8BitDo Ultimate Software V2](https://app.8bitdo.com/Ultimate-Software-V2/).

It is supposed to be started on the screen with the copyright notices. Once started it loads the save file, skips the following recap and starts the fight with a stationary legendary pokemon.

One cycle takes approximately 18.8 seconds.

## Hardware

![image](readme_images/hardware_setup.jpg)

The setup starts with a capture card (not pictured). The card used is a Zasluke 4k USB3.0 HDMI Video Capture-Card. This card converts the HDMI signal of the console and converts it into a usb signal that can be taken in by a [Raspberry Pi 5](https://www.berrybase.de/raspberry-pi-5-1gb-ram). The Raspberry Pi controls an [external board with relays](https://www.waveshare.com/wiki/RPi_Relay_Board) that can (upon termination of the program) cut power to the controller executing the macro.

This is possible, because the used [8BitDo Ultimate 2 Bluetooth Controller](https://www.8bitdo.com/ultimate-2-bluetooth-controller/) was modified on the hardware level. The internal battery was disconnected from the board and an external 4V power supply was connected, via the normally open connection of a relay. That allows to rapidly cut power to the controller and sidesteps the limitations imposed by a battery (finite runtime and charging requirement).

After the power is cut the game isn't reset anymore and the Pokémon can be collected/caught, whenever the next time the operator of the setup checks back in.

## Execution

1. Replicate the hardware setup described above and put the macro on the controller.
2. Start the program and turn the controller on. Reset the game to the starting copyright screen and activate the macro.
3. Wait for success.

## SMS notifications

The program also contains the functionality to send an SMS via the [Twilio](https://www.twilio.com/en-us) service, in case a shiny is found. If this functionality is not desired the struct can just be deleted, without impacting the rest of the program.

## Disclaimer

Even tough the program has been executed over multiple weeks, a success has yet to occur. Any advice or hints as to why would be appreciated.