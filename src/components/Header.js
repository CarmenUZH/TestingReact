import PropTypes from "prop-types"
import Button from "./Button";


const Header = ({title}) => {
    const onClick=() =>{
        console.log("Click")
    }


    return (
        <header className="header">
           <h1 style={headingStyle}>{title}</h1>
            <Button color= "white" text="Report a foking crim" />
            <Button b_col = "yellow" color= "black" text="Piss pants support hotline" onClick={onClick}/>

            {/*How the fuck do i comment */}

        </header>
    )
}

Header.defaultProps={
    title: "Hyper cool title",
    //default if no title provided

}

Header.propTypes={
    title:PropTypes.string,
    //Basically just tell your code to only accept string
}

const headingStyle={
    color:"red",
    backgroundColor:"black"
}

export default Header