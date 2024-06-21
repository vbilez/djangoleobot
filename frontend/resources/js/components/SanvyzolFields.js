import React, { Component, RadioButton,Fragment } from 'react';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox
} from '@material-ui/core';

 export default class SanvyzolFields extends Component {
   constructor(props) {
    super(props);
   }
        
        render(){
          if(this.props.display){
          return (
              <Grid container >
                            <Grid item  md={4}  xs={4} sm={4}>
                                <FormControl>
                                <FormControlLabel
                                    control={
                                        <Checkbox name="dush"  value={this.props.values.dush}  onClick={(event)=>{ this.props.setFieldValue("dush",Boolean(event.target.checked));}}/>
                                    }
                                    label="Душ"
                                    />
                                </FormControl>
                            </Grid>
                            <Grid item  md={4}  xs={4} sm={4}>
                                <FormControl>
                                <FormControlLabel
                                    control={
                                        <Checkbox name="tualet"  value={this.props.values.tualet}  onClick={(event)=>{ this.props.setFieldValue("tualet",Boolean(event.target.checked));}}/>
                                    }
                                    label="Туалет"
                                    />
                                </FormControl>
                            </Grid>
                            <Grid item  md={4}  xs={4} sm={4}>
                                <FormControl>
                                <FormControlLabel
                                    control={
                                        <Checkbox name="vanna"  value={this.props.values.vanna}  onClick={(event)=>{ this.props.setFieldValue("vanna",Boolean(event.target.checked));}}/>
                                    }
                                    label="Ванна"
                                    />
                                </FormControl>
                            </Grid>
                        </Grid>
            );
           }

           else{
             return null;
           }
        }
   }