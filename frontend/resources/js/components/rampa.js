
import React, { Component, RadioButton,Fragment } from 'react';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox
} from '@material-ui/core';

 export default class Rampa extends Component {
   constructor(props) {
    super(props);
   }
        
        render(){
            return(
            <FormControl>
                <FormControlLabel
                control={
                <Checkbox name="rampatwo"  value={this.props.v}  onClick={(event)=>{this.props.setFieldValue("rampatwo",Boolean(event.target.checked));}}/>
                }
                label="Рампа two"
                />
            </FormControl>
            );
        }
   }
 