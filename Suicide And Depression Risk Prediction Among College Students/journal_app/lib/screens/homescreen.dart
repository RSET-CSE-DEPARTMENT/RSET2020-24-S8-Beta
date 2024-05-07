import 'package:flutter/material.dart';
import 'package:journal_app/screens/add_entry_screen.dart';
import 'package:journal_app/screens/loginsignup/login.dart';
import 'package:journal_app/screens/readList_screen.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../constants.dart';
import '../components.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
class HomeScreen extends StatefulWidget {
   const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String? username;
  String? classname;
  String? name;
  @override
  void initState() {
    super.initState();
     _loadSharedPrefs(); // Load the QR code image when the home page is initialized
  }
  _loadSharedPrefs() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      username = prefs.getString('username');
      classname = prefs.getString('classname');
      name = prefs.getString('name');
    });
  }
  @override
  Widget build(BuildContext context) {
    final w = MediaQuery.of(context).size.width;
    final h = MediaQuery.of(context).size.height;
    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
        backgroundColor: Colors.lightBlue,
        title: const Text('Home'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
             signout(context);
            },
          ),
        ],
      ),
        body: Container(
          width: w,
          height: h,
          decoration: kScreenBg,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              JournyTitle(),
              const SizedBox(
              height: 30,
            ),
            SizedBox(
              width: double.infinity,
              child: Text(
                '   Welcome,$username',
                style: const TextStyle(fontSize: 35, fontWeight: FontWeight.bold,color: Color.fromARGB(255, 223, 220, 209)),
                textAlign: TextAlign.left,
              ),
            ),
              SizedBox(
                height: h * 0.045,
              ),
              Image(
                image: AssetImage('images/diary.png'),
                width: w * 0.51,
                height: h * 0.23,
              ),
              SizedBox(
                height: h * 0.08,
              ),
              JournyButton(
                label: 'Read Entries',
                fn: ()async {
                  final path1 = 'diary/$classname/$username/history/history';
                  await FirebaseFirestore.instance.collection(path1).get().then((snapshot) {List<QueryDocumentSnapshot> docList=snapshot.docs;
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => ReadEntryList(docs: docList),
                      ),
                    ); });
                }
              ),
              SizedBox(
                height: 20,
              ),
              JournyButton(
                label: 'Add Entry',
                 fn: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context)=>AddEntryScreen(username: username,classname: classname,),),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
  signout(BuildContext ctx) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    Navigator.of(ctx).pushAndRemoveUntil(
      MaterialPageRoute(builder: (ctx1) =>  LoginScreen2()),
      (route) => false,
    );
  }
}