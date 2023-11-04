const express=require("express");
const bodyparser=require("body-parser");
const https=require("https");
const app=express();
app.use(express.static("./frontend"));
app.use(express.static("/public"));
app.use(bodyparser.urlencoded({extended:true}));
const mongoose=require("mongoose");
require('dotenv').config();
mongoose.connect(process.env.mongodb_url,{useNewUrlParser:true});

const userSchema={
   fname:String,
   lname:String,
   email:String,
   password:String,
   status:String
 };

const list=mongoose.model("user",userSchema);

app.get("/",function(req,res){
    res.sendFile(__dirname+"/frontend/home.html");
});

app.get("/signup",function(req,res){
   res.sendFile(__dirname+"/frontend/signup.html");
});

app.get("/signin",function(req,res){
   res.sendFile(__dirname+"/frontend/signin.html");
});

app.get("/teacher",function(req,res){
   res.sendFile(__dirname+"/frontend/teacher.html");
});

app.get("/student",function(req,res){
   res.sendFile(__dirname+"/frontend/student.html");
});

app.get("/success",function(req,res){
   res.sendFile(__dirname+"/frontend/success.html");
});

app.post("/upload",function(req,res){
   res.redirect("/success");
});
app.post("/upload1",function(req,res){
   res.redirect("/success");
});
app.post("/upload2",function(req,res){
   res.redirect("/success");
});
app.post("/upload3",function(req,res){
   res.redirect("/success");
});
app.post("/upload4",function(req,res){
   res.redirect("/success");
});

app.post("/signin",function(req,res){
   const email=req.body.email;
   const pass=req.body.password;
  async function finduser(){
    const found=await list.find({email:email,password:pass})
   console.log(found);
   if(found){
      found.forEach(function(find){
         console.log(find.status);
         const stat=find.status;
         if(find.status=="teacher"||find.status=="Teacher"||find.status=="TEACHER"){
            res.redirect("/teacher");}
            else{
             res.redirect("/student");}
     });
      
   }
  }
  finduser();
}); 



app.post("/signup",function(req,res){
   const lname=req.body.lname;
   const fname=req.body.fname;
   const email=req.body.email;
   const pass=req.body.password;
   const status=req.body.status;
   console.log(lname);
   console.log(fname);
   console.log(email);
   console.log(pass);
   console.log(status);
   const user=new list({
      fname:req.body.fname,
      lname:req.body.lname,
      email:req.body.email,
      password:req.body.password,
      status:req.body.status
  }); 

  
  user.save();
  if(status=="teacher"||status=="Teacher"||status=="TEACHER"){
  res.redirect("/teacher");}
  else{
   res.redirect("/student");
  }
});
 
const port=process.env.PORT;

app.listen(port,()=>{
    console.log(`Server started at port ${port}`);
 });