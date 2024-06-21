
import React, { Component, RadioButton,Fragment } from 'react';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox
} from '@material-ui/core';

 export default class KstsanvuzlivField extends Component {
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
                                error={this.props.touched.kstsanvuzliv && Boolean(this.props.errors.kstsanvuzliv)}
                                label="К-сть санвузлів"
                                name="kstsanvuzliv"
                                id="kstsanvuzliv"
                                value={this.props.values.kstsanvuzliv}
                                margin={"dense"}
                                onChange={(e)=>{this.props.handleChange(e);
                                
                                }}

                                placeholder="Виберіть к-сть санвузлів"
                                >
                                <MenuItem value={1}>1</MenuItem>
                                <MenuItem value={2}>2</MenuItem>
                                <MenuItem value={3}>3</MenuItem>
                                <MenuItem value={4}>4</MenuItem>
                                <MenuItem value={5}>5+</MenuItem>
                            </TextField>
                        </FormControl>
               
            );
           }

           else{
             return null;
           }
        }
   }