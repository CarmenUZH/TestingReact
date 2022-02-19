import './App.css';
import { useState, useEffect } from "react"
import Header from "./components/Header"
import Footer from "./components/Footer";
import Tasks from "./components/Tasks";
import AddTask from "./components/AddTask";
import Button_Task from "./components/Button_Task";
import React from 'react';
import{ BrowserRouter as Router, Route, Routes, Link} from "react-router-dom"
import About from "./components/About"

function App() {
    const name = "hammond"
    const show_name = "Bo'om Gea"
    const [showAddTask, setShowAddTask] = useState(false)
    const[tasks, setTasks] = useState([])

    useEffect(() => { //get Data from backendBABYYYY
     const getTasks = async () => {
         const tasksFromServer = await fetchTasks()
         setTasks(tasksFromServer)
     }
      getTasks()
    }, [])

    //fetch tasks
    const fetchTasks = async () => {
        const res = await fetch("http://localhost:5000/tasks")
        const data = await res.json()

        return data
    }

    //fetch task singular
    const fetchTask = async (id) => {
        const res = await fetch(`http://localhost:5000/tasks/${id}`)
        const data = await res.json()

        return data
    }
//Add Task
    const addTask = async (task) =>{
    const res = await fetch("http://localhost:5000/tasks", {
        method: "POST", headers:{
            "Content-type":"application/json"
        },
        body: JSON.stringify(task)
    })
        const data = await res.json() //ohne das await keyword können server und front-end nicht syncen bevor front end sich ändert
        setTasks([...tasks, data])

       /* const id = Math.floor(Math.random() * 100 +1)
        const newTask ={id, ...task}
        setTasks([...tasks,newTask])
        console.log(id)
*/
    }


    //Delete Task
    const deleteTask=async (id)=>{
        console.log("delete",id)
        await fetch(` http://localhost:5000/tasks/${id}`,{
            method: "DELETE"
        })
        setTasks(tasks.filter((task)=> task.id !== id))
    }

    //When trying to make a new funciton, its easy to at firts just let it console.log something to see if it reacts when we want it to and then implement "the meat"

    //Toggle Reminder
    const toggleReminder = async (id) =>{
        const taskToToggle = await fetchTask(id)
        const updTask = {...taskToToggle, reminder: !taskToToggle.reminder}

        const res = await fetch(` http://localhost:5000/tasks/${id}`,{
        method: "PUT",
        headers:{
            "Content-type": "application/json"
        },
        body: JSON.stringify(updTask)
    })
        const data = await res.json()

        setTasks(
        tasks.map((task)=>task.id === id ? {...task,reminder: data.reminder} : task))
    }

  return ( <Router>
    <div className="container">
    <Header />

        <h2> my name is {name}</h2>
        <h2> and this is {show_name}</h2>
        <img style={{display:"flex",minWidth:"300px"}}  src="https://i.kym-cdn.com/photos/images/original/001/900/613/e55.jpg"/>
        {tasks.length> 0 ? (<Tasks tasks = {tasks} onDelete={deleteTask} onToggle={toggleReminder} /> ):( "you have no tasks, m8" )}
        <Button_Task onAdd={()=>setShowAddTask(!showAddTask)}
                     showAdd={showAddTask}
        />
        {showAddTask && <AddTask onAdd={addTask} />}
        {/*<Routes>
            <Route path = "/about" exact component = {About}/>
        </Routes> */}
            <Footer/>
    </div>
      </Router>
  );
}
//couldn't yet figure out how to get routes to work
export default App;
