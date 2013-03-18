#!/usr/bin/perl

# Alptugay Değirmencioğlu
# alptugay@labristeknoloji.com
# A Perl script to execute commands on a remote Cisco device

# Input: A Json config file
# Sample input file format:

#{
#    "ip" : "192.168.0.35",
#    "username" : "Cisco",
#    "password" : "Cisco",
#    "transport_protocol" : "Telnet",
#    "enable_password" : "Cisco",
#    "personality" : "ios",
#
#    "request" : {
#        "enable" : true,
#        "configure" : false,
#        "commands" : [
#           {
#                "command" : "show dot11 bssid"
#            }
#        ]
#    }
#}

# Output: Returned string from remote Cisco device

# ERROR CODES
# This error is given when we cannot connect to a remote device.
# {
# "status":"100",
# "message":"Unable to connect to remote host"
# }
#
# This error is given when an illegal command is given to the remote device.
# {
# "status":"101",
# "message":"% Invalid input detected at '^' marker."
# }
#
# This error is given when a wrong username/password is given.
# {
# "status":"101",
# "message":"% Authentication failed"
# }

use strict;
use warnings;
use Readonly;
use Try::Tiny;
use Net::Telnet;
use Net::Appliance::Session;
use JSON;
use Data::Dumper;

use version; our $VERSION = qv('1.0.0');

# ERROR CODES
Readonly my $NO_ERROR                => 110;
Readonly my $NET_APPLIANCE_ERROR     => 100;
Readonly my $NET_APPLIANCE_EXCEPTION => 101;
Readonly my $FILE_OPEN_ERROR         => 102;
Readonly my $FILE_CLOSE_ERROR        => 103;
Readonly my $UNKNOWN_ERROR           => 104;

# CONSTANTS
Readonly my $MAX_BUFFER_LENGTH => 4_194_304;
Readonly my $SESSION_TIMEOUT   => 1_000;

#Generating JSON object from input file

my $return_json;    # Returned json

my $decoded_json =
  read_input( $ARGV[0] );    # Read input file and return it as a JSON object

########
#Setting parameters according to JSON file

my $_device_ip       = $decoded_json->{'ip'};
my $_ios_username    = $decoded_json->{'username'};
my $_ios_password    = $decoded_json->{'password'};
my $_transport_p     = $decoded_json->{'transport_protocol'};
my $_enable_password = $decoded_json->{'enable_password'};
my $_personality     = $decoded_json->{'personality'};
my $_enable_mode;
my $_configure_mode;

my $error = 0;
if ( $decoded_json->{'request'}->{'enable'} ) {
    $_enable_mode = 1;    # true
}
else {
    $_enable_mode = 0;    # false
}
if ( $decoded_json->{'request'}->{'configure'} ) {
    $_configure_mode = 1;    # true
}
else {
    $_configure_mode = 0;    # false
}

my @_commands = @{ $decoded_json->{'request'}->{'commands'} };
my $return_json_status;      # Status field in the returned json
my $current_command;         # The command being executed in the loop
try {
    ## Opening a session to remote device
    my $session = Net::Appliance::Session->new(
        Host      => $_device_ip,
        Timeout   => $SESSION_TIMEOUT,
        Transport => $_transport_p
    );
    $session->max_buffer_length($MAX_BUFFER_LENGTH);
    $session->do_privileged_mode(1);
    $session->connect( Name => $_ios_username, Password => $_ios_password );
    my $result = execute_in_remote($session);
    print $result;
    $session->close;
}
catch {
    print error_report( $_, $_device_ip );
    exit;
};

# This is the main function where we execute command on remote device and return a json object
# containing a status code and the message received from the remote device
sub execute_in_remote {
    my ($session) = @_;
    my @out
      ;    # The output message from the remote device is held in this variable
    my $message;
    if ($_enable_mode) {
        $session->begin_privileged($_enable_password);    #Enable mode
    }

    if ($_configure_mode) {
        $session->begin_configure;                        #Configure mode
    }
    for my $cmd (@_commands) {
        $current_command = $cmd->{'command'};

# Sometimes we my want to enter or leave configure mode while executing a command array
# This case is handled here
        if ( $cmd->{'configure'} ) {
            if ( $cmd->{'configure'} eq 'start' ) {
                $session->begin_configure;
            }
            elsif ( $cmd->{'configure'} eq 'end' ) {
                $session->end_configure;
            }
        }

# If we are waiting for an output like a confirmation dialog from the remote device
# this is handled here
        if ( $cmd->{'match'} ) {
            my $current_match = $cmd->{'match'};
            @out = $session->cmd(
                String => $current_command,
                Match  => [$current_match]
            );
        }
        else {
            @out = $session->cmd( String => $current_command );
        }
        my $output = join q{}, @out;

        $return_json_status = $NO_ERROR;

        if ( length($output) > 1 ) {
            $message = $output;
        }
    }

    $return_json = { status => $return_json_status, message => $message };

    return to_json($return_json);
}

# standard subroutine used to extract failure info when
# interactive session fails
sub error_report {
    my $err         = shift or croak('No err !');
    my $device_name = shift or croak('No device name !');
    my $message;    # The variable which will hold the error message

    if ( eval { $err->isa('Net::Appliance::Session::Exception') } ) {
        $return_json_status = $NET_APPLIANCE_EXCEPTION;
        $message            = $err->lastline;

    }
    elsif ( eval { $err->isa('Net::Appliance::Session::Error') } ) {

        # fault description from Net::Appliance::Session
        $return_json_status = $NET_APPLIANCE_ERROR;
        $message            = $err->message;

    }
    else {

        # we had some other error that wasn't a deliberately created exception
        $return_json_status = $UNKNOWN_ERROR;
        $message            = $err;
    }
    $return_json = { status => $return_json_status, message => $message };
    return to_json($return_json);
}

# read_input function reads the input and returns a json object
sub read_input {
    my ($in_file) = @_;
    my $json;    # Input json given to this script
    local $/ = undef;
    if ( open my $fh, '<', $in_file ) {
        $json = <$fh>;
        if ( not close $fh ) {
            $return_json = {
                status  => $FILE_CLOSE_ERROR,
                message => "Unable to close $in_file"
            };
            print to_json($return_json);
            exit;
        }
        else {
            return decode_json($json);
        }

    }
    else {
        $return_json = {
            status  => $FILE_OPEN_ERROR,
            message => "Unable to open and read $in_file"
        };
        print to_json($return_json);
        exit;
    }

}
