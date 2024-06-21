
import React, { Component, RadioButton,Fragment } from 'react';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox
} from '@material-ui/core';

 export default class KstrivnivField extends Component {
   constructor(props) {
    super(props);
   }
        
        render(){
          if(this.props.display){
          return (
                        <FormControl>
                            <TextField variant="outlined"
                                style={{marginBottom:"7px"}}
                                select
                                error={this.props.touched.kstrivniv && Boolean(this.props.errors.kstrivniv)}
                                label="Кількість рівнів"
                                name="kstrivniv"
                                id="kstrivniv"
                                value={this.props.values.kstrivniv}
                                margin={"dense"}
                                onChange={(e)=>{this.props.handleChange(e);
                                
                                }}

                                placeholder="Виберіть кількість рівнів"
                                >
                                <MenuItem value={1}>1</MenuItem>
                                <MenuItem value={2}>2</MenuItem>
                                <MenuItem value={3}>3</MenuItem>
                                <MenuItem value={4}>4+</MenuItem>
                            </TextField>
                        </FormControl>
               
            );
           }

           else{
             return null;
           }
        }
   }