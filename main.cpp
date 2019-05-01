#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/SetMode.h>
#include <mavros_msgs/State.h>
#include "std_msgs/String.h"
#include <string>

std::string telegram_msg;
std::string prev_telegram_msg;
void chatterCallback(const std_msgs::String::ConstPtr& msg) {
    telegram_msg = msg->data.c_str();
}

mavros_msgs::State current_state;
void state_cb(const mavros_msgs::State::ConstPtr& msg){
    current_state = *msg;
}

int main(int argc, char **argv) {
    ros::init(argc, argv, "offboard");
    ros::NodeHandle nh;

    ros::Subscriber sub = nh.subscribe("/telegram_bot/telegram_chat", 1000, chatterCallback);
    ros::Subscriber state_sub = nh.subscribe<mavros_msgs::State>("mavros/state", 10, state_cb);
    ros::ServiceClient arming_client = nh.serviceClient<mavros_msgs::CommandBool>("mavros/cmd/arming");
    ros::ServiceClient set_mode_client = nh.serviceClient<mavros_msgs::SetMode>("mavros/set_mode");

    mavros_msgs::SetMode offb_set_mode;
    offb_set_mode.request.custom_mode = "OFFBOARD";
    mavros_msgs::CommandBool arm_cmd;
    arm_cmd.request.value = true;

    ros::Rate rate(20.0);

    // wait for FCU connection
    while(ros::ok() && !current_state.connected){
        ros::spinOnce();
        rate.sleep();
    }

    while(ros::ok()) {
       
	if(current_state.mode != "OFFBOARD") {
            if(set_mode_client.call(offb_set_mode) && offb_set_mode.response.mode_sent) ROS_INFO("Offboard enabled");
        }

	if(telegram_msg == "arm") arming_client.call(arm_cmd);

        ros::spinOnce();
        rate.sleep();
    }

    return 0;
}
