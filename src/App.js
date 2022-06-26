import './App.css';
import React, { Component }  from 'react';
import axios from 'axios'

class App extends Component {
  constructor(props){
    super(props);
    this.state={
      originCode:"",
      assemblyCode:"",
      currentCode:""
    };
    
  }
  componentDidMount(){
    
  }
  updateCode = (e) =>{
    this.setState({
      originCode:e.target.value 
    },()=>{
      // console.log(e.target.value);
    })
  }

  convertCode = () =>{
    console.log(this.state.originCode);
    let transformText = this.state.originCode.replaceAll("\n","(enter)").replaceAll("\t","(tab)");
    //Convert Code 
    fetch(`/dis?code=${transformText}`).then(res => res.json()).then(data =>{
      console.log(data);
      this.setState({
        currentCode:data.code,
      },()=>{
        //Insert it into Assembly TextArea
        var targetDOM = document.getElementById('asm-code').getElementsByTagName('textarea')[0];
        targetDOM.value = this.state.currentCode;
      })
    });

    
  }

  formatCode = (e) =>{
    if(e.keyCode === 9){
      e.preventDefault();
      e.target.value = e.target.value + "\t";
      
    }
    if(e.keyCode === 13){
      var lastSymbol = e.target.value[e.target.value.length - 1];
      if(lastSymbol === ":"){
        e.preventDefault();
        e.target.value = e.target.value  + "\n\t";
      }
    }
  }

  render(){
    return(
      <div className="App">
        <div className="form-floating" id="origin-code">
          <textarea className="form-control" placeholder="Leave a comment here" id="floatingTextarea2" style={{height: "100px"}} value={this.state.convertCode} onChange={(e)=>this.updateCode(e)} onKeyDown={(e)=>this.formatCode(e)}></textarea>
          <label htmlFor="floatingTextarea2">Origin-code</label>
        </div>
        <button type="button" className="btn btn-outline-primary m-4" id="convert-code" onClick={()=>this.convertCode()}>Convert</button>
        <div className="form-floating" id="asm-code">
          <textarea className="form-control" placeholder="Leave a comment here" id="floatingTextarea2" style={{height: "100px"}}></textarea>
          <label htmlFor="floatingTextarea2">Assembly-code</label>
        </div>
    </div>
    )
  }
}

export default App;
