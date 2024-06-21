
import React, { Component, RadioButton,Fragment } from 'react';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox
} from '@material-ui/core';

 export default class KstspalenField extends Component {
   constructor(props) {
    super(props);
   }
        
        render(){
          if(this.props.display){
          return (
                         <FormControl>
                            <TextField variant="outlined" required
                            style={{marginBottom:"7px"}}
                            select
                            error={this.props.touched.kstspalen && Boolean(this.props.errors.kstspalen)}
                            label="Кількість спалень"
                            name="kstspalen"
                            id="kstspalen"
                            value={this.props.values.kstspalen}
                            margin={"dense"}
                            onChange={(e)=>{this.props.handleChange(e);
                                
                            }}

                            placeholder="Виберіть к-сть спалень"
                            >
                            <MenuItem value={1}>студіо</MenuItem>
                            <MenuItem value={2}>1</MenuItem>
                            <MenuItem value={3}>2</MenuItem>
                            <MenuItem value={4}>3</MenuItem>
                            <MenuItem value={5}>4</MenuItem>
                            <MenuItem value={5}>5</MenuItem>
                            <MenuItem value={5}>6+</MenuItem>
                        </TextField>
                    </FormControl>
               
            );
           }

           else{
             return null;
           }
        }
   }