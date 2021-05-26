import 'dart:convert';
import 'dart:typed_data';
import 'package:flex_color_picker/flex_color_picker.dart';
import 'package:flutter/material.dart';
import 'package:image_gallery_saver/image_gallery_saver.dart';
import 'package:sm_flutter/Widgets/BottomBar.dart';
import 'dart:io';
import 'package:image_picker/image_picker.dart';

class ColorPickerPage extends StatefulWidget {
  static const routeName = '/colorPicker';

  @override
  _ColorPickerPageState createState() => _ColorPickerPageState();
}

class _ColorPickerPageState extends State<ColorPickerPage> {
  // Color for the picker in a dialog using onChanged.
  Color dialogPickerColor;
  final picker = ImagePicker();
  File imatge;
  var imageByte;
  Image letsgoo;
  var llistaRoba;
  int index;
  int textureID;
  bool lastColor = true;

  final List<Map> textures = [
    {'id': 0, 'path': 'lib/img/blue_feathers2.jpg'},
    {'id': 1, 'path': 'lib/img/heads2.jpg'},
    {'id': 2, 'path': 'lib/img/olivo2.png'},
  ];

  Future<bool> colorPickerDialog() async {
    return ColorPicker(
      // Use the dialogPickerColor as start color.
      color: dialogPickerColor,
      // Update the dialogPickerColor using the callback.
      onColorChanged: (Color color) => setState(() {
        dialogPickerColor = color;
        lastColor = true;
      }),
      width: 40,
      height: 40,
      borderRadius: 4,
      spacing: 5,
      runSpacing: 5,
      wheelDiameter: 155,
      heading: Text(
        'Select color',
        style: Theme.of(context).textTheme.subtitle1,
      ),
      subheading: Text(
        'Select color shade',
        style: Theme.of(context).textTheme.subtitle1,
      ),
      wheelSubheading: Text(
        'Selected color and its shades',
        style: Theme.of(context).textTheme.subtitle1,
      ),
      showColorName: true,
      copyPasteBehavior: const ColorPickerCopyPasteBehavior(
        longPressMenu: true,
      ),
      materialNameTextStyle: Theme.of(context).textTheme.caption,
      colorNameTextStyle: Theme.of(context).textTheme.caption,
      colorCodeTextStyle: Theme.of(context).textTheme.caption,
      pickersEnabled: const <ColorPickerType, bool>{
        ColorPickerType.primary: true,
        ColorPickerType.accent: true,
        ColorPickerType.wheel: true,
      },
    ).showPickerDialog(
      context,
      constraints:
          const BoxConstraints(minHeight: 460, minWidth: 300, maxWidth: 320),
    );
  }

  Future<bool> textureDialog() async {
    SimpleDialog alert = SimpleDialog(
      title: Text("Select texture"),
      children: [
        Padding(
          padding: EdgeInsets.all(40),
          child: Column(

            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ...(textures.map((i) {
                    return Container(
                      width: 44,
                      height: 44,
                      decoration: BoxDecoration(
                          border: Border.all(
                            color: Colors.black,
                          ),
                          borderRadius: BorderRadius.all(Radius.circular(4))),
                      child: Stack(
                        children: [
                          InkWell(
                            onTap: () {
                              setState(() {
                                textureID = i['id'];
                                lastColor = false;
                              });

                            },
                            child: Image(
                              image: AssetImage(i['path']),
                              fit: BoxFit.fill,
                            ),
                          ),
                        ],
                      ),
                    );
                  })).toList(),
                ],
              )
            ],
          ),
        ),
        SimpleDialogOption(
          onPressed: () {
            Navigator.of(context).pop();
          },
          child: const Text(
            'OK',
            style: TextStyle(
              fontSize: 15,
              color: Colors.blue,

            ),
            textAlign: TextAlign.end,
          ),
        ),
      ],
    );

    showDialog(
        context: context,
        builder: (BuildContext context) {
          return alert;
        });
  }

  Future<bool> colorTextureDialog() async {
    SimpleDialog alert = SimpleDialog(
      title: Text("Color or texture"),
      children: [
        Padding(
          padding: EdgeInsets.all(40),
          child: Column(
            //mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                Container(
                  color: Colors.white,
                  child: ColorIndicator(
                    width: 44,
                    height: 44,
                    borderRadius: 4,
                    color: dialogPickerColor,
                    onSelectFocus: false,
                    onSelect: () async {
                      Navigator.of(context).pop();
                      // Store current color before we open the dialog.
                      final Color colorBeforeDialog = dialogPickerColor;
                      // Wait for the picker to close, if dialog was dismissed,
                      // then restore the color we had before it was opened.
                      if (!(await colorPickerDialog())) {
                        setState(() {
                          dialogPickerColor = colorBeforeDialog;
                        });
                      }
                    },
                  ),
                ),
                Container(
                  width: 44,
                  height: 44,
                  decoration: BoxDecoration(
                      border: Border.all(
                        color: Colors.black,
                      ),
                      borderRadius: BorderRadius.all(Radius.circular(4))),
                  child: InkWell(
                    onTap: () {
                      Navigator.of(context).pop();
                      textureDialog();
                    },
                    child: Image(
                      image: AssetImage(textures[textureID]['path']),
                      fit: BoxFit.cover,
                    ),
                  ),
                ),
              ]),
            ],
          ),
        ),
        SimpleDialogOption(
          onPressed: () {
            Navigator.of(context).pop();
          },
          child: const Text(
            'OK',
            style: TextStyle(
              fontSize: 15,
              color: Colors.blue,

            ),
            textAlign: TextAlign.end,
          ),
        ),
      ],
    );

    showDialog(
        context: context,
        builder: (BuildContext context) {
          return alert;
        });
  }

  Future getImageGallery() async {
    final pickedFile = await picker.getImage(source: ImageSource.gallery);
    imatge = File(pickedFile.path);
    setState(() {
      if (pickedFile != null) {
        imatge = File(pickedFile.path);
        letsgoo = Image.file(imatge);
        imageByte = imatge.path;
        sendFile();
      } else {
        print('No image selected.');
      }
    });
  }

  Future<File> getImageCamera() async {
    final pickedFile = await picker.getImage(source: ImageSource.camera);
    imatge = File(pickedFile.path);
    setState(() {
      if (pickedFile != null) {
        imatge = File(pickedFile.path);
        letsgoo = Image.file(imatge);
        imageByte = imatge.path;
      } else {
        print('No image selected.');
      }
    });
  }

  void sendFile() async {
    List<int> imageBytes = imatge.readAsBytesSync();

    final Map jsonMap = {"image": imageBytes};
    //final String url = 'http://10.0.2.2:5000/getImage';
    final String url = 'https://onetapfashionista.oa.r.appspot.com/getImage';
    HttpClient httpClient = new HttpClient();
    HttpClientRequest request = await httpClient.postUrl(Uri.parse(url));
    request.headers.set('content-type', 'application/json');
    request.add(utf8.encode(json.encode(jsonMap)));
    HttpClientResponse response = await request.close();

    String reply = await response.transform(utf8.decoder).join();

    if (jsonDecode(reply)['res'] == 'ok') {
      setState(() {
        llistaRoba = jsonDecode(reply)['llista']; //list of map
        index = llistaRoba[0]['icon'];
      });
    } else {
      print('Llista no disponible');
    }
  }

  void obtenirImage(BuildContext context) async {
    final Map jsonMap = {
      "roba": index,
      'isColor': lastColor,
      'color': '#${dialogPickerColor.value.toRadixString(16).substring(2, 8)}',
      'textura': textureID
    };
    //final String url = 'http://10.0.2.2:5000/returnImage';
    final String url = 'https://onetapfashionista.oa.r.appspot.com/returnImage';
    HttpClient httpClient = new HttpClient();
    HttpClientRequest request = await httpClient.postUrl(Uri.parse(url));
    request.headers.set('content-type', 'application/json');
    request.add(utf8.encode(json.encode(jsonMap)));
    HttpClientResponse response = await request.close();
    String reply = await response.transform(utf8.decoder).join();

    
    setState(() {
      imageByte = Uint8List.fromList(jsonDecode(reply)['imatge'].cast<int>());
      letsgoo = Image.memory(
          Uint8List.fromList(jsonDecode(reply)['imatge'].cast<int>()));
    });
    //httpClient.close();
  }

  @override
  void initState() {
    super.initState();
    dialogPickerColor = Colors.red; // Material red.
    textureID = 0;
  }

  int count = 0;

  void initImage() {
    if (count < 1) {
      final int inputType = ModalRoute.of(context).settings.arguments;
      if (inputType == 1) {
        getImageCamera();
      } else {
        getImageGallery();
      }
      count += 1;
    }
  }

  callback(newAbc) {
    setState(() {
      index = newAbc;
    });
  }


  @override
  Widget build(BuildContext context) {
    initImage();
    return Scaffold(
      appBar: AppBar(
        title: Text('Choose the color'),
        toolbarHeight: 70,
        actions: <Widget>[
          Padding(
            padding: EdgeInsets.only(right: 20.0),
            child: InkWell(
              onTap: () {
                imageByte.runtimeType == String
                    ? ImageGallerySaver.saveFile(imageByte)
                    : ImageGallerySaver.saveImage(imageByte);
                // TODO ALERT IMAGE SAVED
              },
              child: Icon(
                Icons.save,
                size: 50,
              ),
            ),
          ),
        ],
      ),
      body: Stack(children: [
        Container(
          width: MediaQuery.of(context).size.width,
          height: MediaQuery.of(context).size.height - 170,
          child: Padding(
            padding: EdgeInsets.all(20),
            child: letsgoo == null
                ? Text('No image selected.')
                : Image(
                    image: letsgoo.image,
                    fit: BoxFit.contain,
                  ),
          ),
        ),
        Positioned(
          bottom: 10,
          right: 20,
          child: Container(
            width: 44,
            height: 44,
            decoration: BoxDecoration(
                border: Border.all(
                  color: Colors.transparent,
                ),
                borderRadius: BorderRadius.all(Radius.circular(4))),
            child: InkWell(
              onTap: () {
                colorTextureDialog();
              },
              child: lastColor == true
                  ? Container(
                      color: dialogPickerColor,
                    )
                  : Image(
                      image: AssetImage(textures[textureID]['path']),
                    ),
            ),
          ),
        ),
      ]),
      bottomNavigationBar: llistaRoba == null
          ? Text('loading')
          : BottomBar(llistaRoba: llistaRoba, Callback: callback),
      floatingActionButton: FloatingActionButton(

        child: Icon(Icons.play_arrow),
        onPressed: () {
          obtenirImage(context);
        },
      ),
      floatingActionButtonLocation:
          FloatingActionButtonLocation.centerFloat,
    );
  }
}
