
import React, { Component, RadioButton,Fragment } from 'react';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox
} from '@material-ui/core';

 export default class KimnatavkvartyriField extends Component {
   constructor(props) {
    super(props);
   }
        
        render(){
          if(this.props.display){
          return (
                         <FormControl>
                            <FormControlLabel
                                control={
                                    <Checkbox name="kimnatavkvartyri"  value={this.props.values.kimnatavkvartyri}  onClick={(event)=>{ this.props.setFieldValue("kimnatavkvartyri",Boolean(event.target.checked));}}/>
                                }
                                label="Кімната в квартирі"
                                />
                        </FormControl>
               
            );
           }

           else{
             return null;
           }
        }
   }