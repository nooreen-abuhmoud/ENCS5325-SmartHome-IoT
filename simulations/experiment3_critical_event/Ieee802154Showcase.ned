package simulations.experiment3_critical_event;

import inet.node.inet.StandardHost;
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.inet.SensorNode;
import inet.physicallayer.wireless.ieee802154.packetlevel.Ieee802154NarrowbandScalarRadioMedium;
import inet.visualizer.canvas.integrated.IntegratedMultiCanvasVisualizer;

network CriticalEventNetwork
{
   	parameters:
        int numSensors = default(5);
        @display("bgb=20,20;bgi=showcases/floorplan,s");
    submodules:
 		sensor[numSensors]: SensorNode {
    		@display("i=misc/sensor;t=Sensor");
		}
        lamp1: SensorNode {
            @display("p=8,5;i=status/bulb;t=Light 1");
        }
        lamp2: SensorNode {
            @display("p=8.75,13.5;i=status/bulb;t=Light 2");
        }
        lamp3: SensorNode {
            @display("p=13.5,8.5;i=status/bulb;t=Light 3");
        }
        lamp4: SensorNode {
            @display("p=16.5,9.5;i=status/bulb;t=Light 4");
        }
        lamp5: SensorNode {
            @display("p=13.5,14;i=status/bulb;t=HVAC");
        }
        lamp6: SensorNode {
            @display("p=4,13;i=status/bulb;t=Alarm");
        }
        lamp7: SensorNode {
            @display("p=4,10.5;i=status/bulb;t=Smart Plug");
        }
        lamp8: SensorNode {
            @display("p=4,5;i=status/bulb;t=Door Lock");
        }

        controller: SensorNode {
    		parameters:
        		numPppInterfaces = 1;
        		forwarding = true;
        		@display("p=6.5,10.5;i=misc/sensorgateway;t=IoT Gateway");
		}
		
		monitoringServer: StandardHost {
    		parameters:
        		numPppInterfaces = 1;
        		@display("p=18,6;i=device/server;t=Core Monitoring Server");
		}
        configurator: Ipv4NetworkConfigurator {
            @display("p=18,0.75");
        }
        radioMedium: Ieee802154NarrowbandScalarRadioMedium {
            @display("p=18,2.25");
        }
        visualizer: IntegratedMultiCanvasVisualizer {
            @display("p=18,3.75");
        }
        connections:
            controller.pppg[0] <--> {
                delay = 1ms;
                datarate = 100Mbps;
            } <--> monitoringServer.pppg[0];
}
