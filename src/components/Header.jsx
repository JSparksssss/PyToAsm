import React, { Component } from 'react';
import Logo from "../../src/static/logo.png"

class Header extends Component{
    constructor(props){
        super(props)
    }

    render(){
        return(
            <nav class="navbar navbar-light bg-dark">
            <a class="navbar-brand" href="#">
                <img src={Logo} width="120" height="30" alt=""/>
            </a>
            </nav>
        )
    }
}

export default Header;