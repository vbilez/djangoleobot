
import React, { Component, RadioButton,Fragment } from 'react';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox
} from '@material-ui/core';

 export default class VilneplanuvanniaField extends Component {
   constructor(props) {
    super(props);
   }
        
        render(){
          if(this.props.display){
          return (
                         <FormControl>
                            <FormControlLabel
                                control={
                                    <Checkbox name="vilneplanuvannia"  value={this.props.values.vilneplanuvannia}  onClick={(event)=>{ this.props.setFieldValue("vilneplanuvannia",Boolean(event.target.checked));}}/>
                                }
                                label="Вільне планування"
                                />
                        </FormControl>
            );
           }

           else{
             return null;
           }
        }
   }