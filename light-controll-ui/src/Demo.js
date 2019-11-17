import React, {Component} from 'react'
import Roundy from 'roundy';
import axios from 'axios';
import {makeStyles} from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';


export class Demo extends Component {
    RELAXATION_BRIGHTNESS = 20;
    RELAXATION_TEMPERATURE = 3400;

    EVENING_BRIGHTNESS = 30;
    EVENING_TEMPERATURE = 3900;

    FOCUS_BRIGHTNESS = 60;
    FOCUS_TEMPERATURE = 5000;

    WAKEUP_BRIGHTNESS = 40;
    WAKEUP_TEMPERATURE = 6000;


    constructor(props) {
        super(props);
        this.state = {
            max: 100,
            min: 0,
            color: '#00ff00',
            step: 10,
            brightness: 30,
            color_temperature: 5100,
            radius: 100,
            device_id: "EC22"
        };
        const tmp = this;
        axios.get('http://localhost:8070/api/v1/get_state')
            .then(function (response) {
                console.log(response);
                if (response.data) {
                    tmp.setState({brightness: response.data[tmp.state.device_id].settings.light_level_value});
                    tmp.setState({color_temperature: response.data[tmp.state.device_id].settings.color_temperature_value});
                }
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    updateState() {
        axios.post('http://localhost:8070/api/v1/update_light', {
            device_id: this.state.device_id,
            settings: {
                light_level_value: this.state.brightness,
                color_temperature_value: this.state.color_temperature
            }
        })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    setLight(type, meta) {
        axios.post('http://localhost:8070/api/v1/set_light', {
            device_id: this.state.device_id,
            settings: {
                light_level_value: this.state.brightness,
                color_temperature_value: this.state.color_temperature
            },
            type: type,
            user: "elizaveta",
            meta: meta
        })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    update_brightness(val) {
        console.log("updating brightnesss to " + val);
        this.updateState()
    }

    update_color_temperature(val) {
        console.log("updating color temperature to " + val);
        this.updateState()
    }

    save_brightness(val) {
        console.log("saving brightnesss to " + val);
        this.setLight("brightness")

    }

    save_color_temperature(val) {
        console.log("saving color temperature to " + val);
        this.setLight("color")
    }

    save_settings(meta) {
        this.setLight("preset", meta)
    }

    render() {
        const classes = makeStyles(theme => ({
            root: {
                flexGrow: 1,
            },
            paper: {
                padding: theme.spacing(2),
                textAlign: 'center',
                color: theme.palette.text.secondary,
            },
        }));
        const {max, min, step, radius, color} = this.state;
        return (
            <div className={classes.root}>
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <Paper className={classes.paper}>
                            <h1>Light Control Panel</h1>
                        </Paper>
                    </Grid>
                    <Grid item xs={6}>
                        <Paper className={classes.paper}>
                            <Roundy style={{margin: "20px"}}
                                    allowClick
                                    value={this.state.brightness}
                                    radius={parseInt(radius)}
                                    min={0}
                                    max={100}
                                    color={"#AEFF78"}
                                    stepSize={5}
                                    arcSize={300}
                                    sliced={false}
                                    onChange={brightness => {
                                        this.setState({brightness: brightness}, () => {
                                            this.update_brightness(brightness)
                                        });
                                    }}
                                    onAfterChange={(color_temperature, props) => {
                                        this.setState({brightness: props.value}, () => {
                                            this.save_brightness(props.value)
                                        });
                                    }}
                            />
                        </Paper>
                        <Paper className={classes.paper}>
                            <b>Brightness: {this.state.brightness}</b></Paper>
                    </Grid>
                    <Grid item xs={6}>
                        <Paper className={classes.paper}>
                            <Roundy style={{margin: "20px"}}
                                    allowClick
                                    value={this.state.color_temperature}
                                    radius={parseInt(radius)}
                                    min={2700}
                                    max={6500}
                                    color={"#CC6E4B"}
                                    stepSize={50}
                                    arcSize={300}
                                    sliced={false}
                                    onChange={color_temperature => {
                                        this.setState({color_temperature: color_temperature}, () => {
                                            this.update_color_temperature(color_temperature)
                                        });
                                    }}
                                    onAfterChange={(color_temperature, props) => {
                                        this.setState({color_temperature: props.value}, () => {
                                            this.save_color_temperature(props.value)
                                        });
                                    }}
                            />
                            <Paper className={classes.paper}>
                                <b>Color temperature: {this.state.color_temperature}</b></Paper>
                        </Paper>
                    </Grid>
                    <Grid item xs={6}>
                        <Paper className={classes.paper}>
                            <Button style={{margin: "10px", backgroundColor: "#d08e75"}} variant="contained" color="prima">
                                Cozy evening
                            </Button>
                            <Button style={{margin: "10px", backgroundColor: "#6FB342"}} variant="contained" color="prima" onClick={event => {
                                this.setState({
                                    color_temperature: this.RELAXATION_TEMPERATURE,
                                    brightness: this.RELAXATION_BRIGHTNESS}, () => {
                                    this.save_settings("relaxation")
                                });
                            }}>
                                Relaxation
                            </Button>
                        </Paper>
                    </Grid>

                    <Grid item xs={6}>
                        <Paper className={classes.paper}>
                            <Button style={{margin: "10px", backgroundColor: "#919FFF"}} variant="contained" >
                                Focus time
                            </Button>
                            <Button style={{margin: "10px",backgroundColor: "#bbf495"}} variant="contained">
                                Wakey-morning
                            </Button>
                        </Paper>
                    </Grid>
                    <Grid item xs={6}>

                    </Grid>

                    <Grid item xs={6}>

                    </Grid>
                </Grid>
            </div>
        )
    }


}