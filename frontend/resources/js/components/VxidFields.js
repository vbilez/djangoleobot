import React, { Component, RadioButton,Fragment } from 'react';
import {Container, TextField, FormGroup, Button, RadioGroup, Select, 
        MenuItem, Box, FormControl, Radio,FormControlLabel, Grid, Checkbox
} from '@material-ui/core';

 export default class VxidFields extends Component {
   constructor(props) {
    super(props);
   }
        
        render(){
          if(this.props.display){
          return (
              <React.Fragment>
                    <FormControl>
                        <TextField variant="outlined"
                            style={{marginBottom:"7px"}}
                            select
                            error={this.props.touched.vxid && Boolean(this.props.errors.vxid)}
                            label="Вхід"
                            name="vxid"
                            id="vxid"
                            value={this.props.values.vxid}
                            margin={"dense"}
                            onChange={(e)=>{this.props.handleChange(e);
                                
                            }}

                            placeholder="Виберіть вхід"
                            >
                            <MenuItem value={1}>фасадний</MenuItem>
                            <MenuItem value={2}>парадний</MenuItem>
                            <MenuItem value={3}>по балкону</MenuItem>
                            <MenuItem value={4}>з двору</MenuItem>
                            <MenuItem value={5}>з чорного входу</MenuItem>
                        </TextField>
                    </FormControl>
                    <FormControl>
                        <TextField variant="outlined"
                          style={{marginBottom:"7px"}}
                          select
                          error={this.props.touched.vxidv && Boolean(this.props.errors.vxidv)}
                          label="Вхід в"
                          name="vxidv"
                          id="vxidv"
                          value={this.props.values.vxidv}
                          margin={"dense"}
                          onChange={(e)=>{this.props.handleChange(e);
                              
                          }}

                          placeholder="Виберіть вхід"
                          >
                          <MenuItem value={1}>кухню</MenuItem>
                          <MenuItem value={2}>кімнату</MenuItem>
                          <MenuItem value={3}>коридор</MenuItem>
                        </TextField>
                    </FormControl>
                    </React.Fragment>
            );
           }

           else{
             return null;
           }
        }
   }