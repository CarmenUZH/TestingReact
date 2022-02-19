import './App.css';
import { useState } from "react"
import Header from "./components/Header"
import Footer from "./components/Footer";
import Tasks from "./components/Tasks";
import AddTask from "./components/AddTask";

function App() {
    const name = "hammond"
    const show_name = "Bo'om Gea"
    const[tasks, setTasks] = useState([
        {id:2,text:"Today i finally find waldo",day:"FRIDAY", reminder: true},
        {id:3,text:"james pisses his pants",day:"SUNDAY", reminder: false},
        {id:4,text:"and i forget the name of the third guy on the team",day:"MONDAY", reminder: true}
    ])




    //Delete Task
    const deleteTask=(id)=>{
        console.log("delete",id)
        setTasks(tasks.filter((task)=> task.id !== id))
    }

    //When trying to make a new funciton, its easy to at firts just let it console.log something to see if it reacts when we want it to and then implement "the meat"
    //Toggle Reminder
    const toggleReminder = (id) =>{

        setTasks(tasks.map((task)=>task.id === id ? {...task,reminder: !task.reminder} : task))
        console.log(id)
    }

  return (
    <div className="container">
    <Header />

        <h2> my name is {name}</h2>
        <h2> and this is {show_name}</h2>
        <img style={{display:"flex",minWidth:"300px"}}  src="https://i.kym-cdn.com/photos/images/original/001/900/613/e55.jpg"/>
        {tasks.length> 0 ? (<Tasks tasks = {tasks} onDelete={deleteTask} onToggle={toggleReminder} /> ):( "you have no tasks, m8" )}
        <AddTask/>
        <Footer/>
    </div>
  );
}

export default App;
