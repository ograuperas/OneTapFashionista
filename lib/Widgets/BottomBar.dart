import 'package:flutter/material.dart';
import 'package:hexcolor/hexcolor.dart';
import 'package:sm_flutter/icons/my_flutter_app_icons.dart';


class BottomBar extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
      backgroundColor: HexColor('#75CD9B'),
      items: <BottomNavigationBarItem>[
        BottomNavigationBarItem(
          icon: Icon(MyFlutterApp.trousers),
          label: 'Trousers',
        ),
        BottomNavigationBarItem(
          icon: Icon(MyFlutterApp.tshirt),
          label: 'T-shirt',
        ),
        BottomNavigationBarItem(
          icon: Icon(MyFlutterApp.shoe1),
          label: 'Shoes',
        ),
      ],
      selectedItemColor: Colors.red,
      onTap: (int) {},
    );
  }
}