
//import 'package:busti007/main.dart';
//import 'package:busti007/screens/homescreen.dart';
//import 'package:busti007/screens/login_conductor.dart';
//import 'package:busti007/screens/welcome.dart';
// import 'package:bus_t/screens/loginsignup/welcome.dart';
// import 'package:bus_t/screens/passsenger/home.dart';
import 'package:flutter/material.dart';
import 'package:journal_app/screens/homescreen.dart';
import 'package:journal_app/screens/loginsignup/login.dart';
import 'package:journal_app/screens/teacherscreen.dart';
import 'package:shared_preferences/shared_preferences.dart';

// import '../conductor/c_home.dart';


class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {

@override
  void initState() {   // splash screen initial 
    checkUserLoggedin();// TODO: implement initState
    super.initState();
  }

@override
  void didChangeDependencies() {
    // TODO: implement didChangeDependencies
    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Image.asset('images/diary.png',
        height: 250,),
      ),
      );
  }
  @override
  void dispose() {
    // TODO: implement dispose
    super.dispose();
  }

  Future<void> gotoLogin() async{
    await Future.delayed(const Duration(seconds: 3));
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (ctx) => LoginScreen2(),
      ),
      );
  }

   Future<void> checkUserLoggedin() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String? username = prefs.getString('username');
    final String? role = prefs.getString('role');
    if (username == null && role == null) {
       gotoLogin();
    } 
//     // else if(busno == null){
//     //    gotoLogin();
//     // }
    else if(role == 'student'){
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (ctx1) =>  HomeScreen()),);
    }
    else if(role == 'teacher'){
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (ctx1) =>  teacherscreen()),);
    }
//     else
//     {
//        Navigator.of(context).pushReplacement(
//         MaterialPageRoute(builder: (ctx1) => ConductorHomePage(busID: busno ??'',)),);
//     }
   }
 }