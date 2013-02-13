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
# "status":"101",
# "message":"Unable to connect to remote host"
# }
#
# This error is given when an illegal command is given to the remote device.
# {
# "status":"100",
# "message":"% Invalid input detected at '^' marker."
# }
#
# This error is given when a wrong username/password is given.
# {
# "status":"100",
# "message":"% Authentication failed"
# }

use strict;
use warnings;

use Net::Telnet;
use Net::Appliance::Session;
use JSON;
use Data::Dumper;

#Generating JSON object from input file

my $json;
{
  local $/; #Enable 'slurp' mode
  open my $fh, "<", $ARGV[0];
  $json = <$fh>;
  close $fh;
}

my $decoded_json = decode_json($json);

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


if ($decoded_json->{'request'}->{'enable'}){
    $_enable_mode = 1; # true
}
else{
    $_enable_mode = 0; # false
}
if ($decoded_json->{'request'}->{'configure'}){
    $_configure_mode = 1; # true
}
else{
    $_configure_mode = 0; # false
}

my @_commands = @{$decoded_json->{'request'}->{'commands'}};

eval {
    #print $_device_ip."\n";
    #print $_transport_p."\n";
    #print $_ios_username."\n";
    #print $_ios_password."\n";
    #print $_enable_password."\n";
    #print $_enable_mode."\n";
    #print $_configure_mode."\n";

    ## Opening a session to remote device
    my $session = Net::Appliance::Session->new(
        Host        => $_device_ip,
        Transport   => $_transport_p
    );

    $session->do_privileged_mode(1);
    $session->connect( Name => $_ios_username, Password => $_ios_password );
    execute_in_remote($session);
    $session->close;
};

#Error Handling
if ($@) {
    print error_report( $@, $_device_ip );
}

sub execute_in_remote {
    my $session = $_[0];

    if ($_enable_mode){
        $session->begin_privileged($_enable_password);    #Enable mode
    }

    if ($_configure_mode){
        $session->begin_configure;                        #Configure mode
    }

    for my $cmd (@_commands) {
        #print $cmd->{'command'}."\n";
        my @out = $session->cmd($cmd->{'command'});
        #print @out;
        my $output = join "", @out;
        my $response = { status => 110, message => $output };
        print to_json($response);
        #print "{\n".'"status":'.'"110"'.",\n".'"message":'.'"'. $output .'"'."\n}";
    }
}


sub error_report {

    # standard subroutine used to extract failure info when
    # interactive session fails

    my $err         = shift or croak("No err !");
    my $device_name = shift or croak("No device name !");

    my $report;    # holder for report message to return to caller

    if ( UNIVERSAL::isa( $err, 'Net::Appliance::Session::Exception' ) ) {
        $report = "{\n".'"status":'.'"100"'.",\n".'"message":'.'"'.$err->lastline .'"'."\n}";
        # fault description from Net::Appliance::Session
        #$report =
#"\nWe had an error during our Telnet/SSH session to device  : $device_name \n";
        #$report .= $err->message . " \n";

        # message from Net::Telnet
        #$report .= "Net::Telnet message : " . $err->errmsg . "\n";

        # last line of output from your appliance
        #$report .=
        #  "Last line of output from device : " . $err->lastline . "\n\n";
    }
    elsif ( UNIVERSAL::isa( $err, 'Net::Appliance::Session::Error' ) ) {

        # fault description from Net::Appliance::Session
        $report = "{\n".'"status":'.'"101"'.",\n".'"message":'.'"'.$err->message .'"'."\n}";
    }
    else {
        $report = "{\n".'"status":'.'"102"'.",\n".'"message":'.'"'.$err .'"'."\n}";
        # we had some other error that wasn't a deliberately created exception
        #$report = "We had an issue when accessing the device : $device_name \n";
        #$report .= "The reported error was : $err \n";
    }

    return $report;
}

