#!/usr/bin/perl
use warnings;
use strict;
use utf8;
use open IO => ':encoding(UTF-8)', ':std';
use feature qw{ say signatures };
use JSON qw( decode_json  encode_json to_json from_json);

no warnings qw{ experimental::signatures };
my $home = $ENV{HOME};
chomp( my $date   = `date +'%Y-%m-%d_%H.%M.%S'` );
chomp( my $hour   = `date +'%H'` );
chomp( my $minute = `date +'%M'` );
my $hasargs = $#ARGV;
my $help    = "";
my $string  = "";
my $set     = "";
use Getopt::Long;
my $force  = "";
my $force2 = "";
GetOptions(
    "string=s" => \$string,
    "help"     => \$help,
    "set"      => \$set,
    "force"    => \$force,
    "force2"   => \$force2,
) or die("Error in command line arguments\n");

my %settings = %{ from_json(`cat /home/ilce/bin/pijuice_tools/settings.json`) };

if ($set) {

    # For testing...
    if ( !$hasargs ) {
        say
"Usage: $0 --set hour_for_wakeup minute_forwakeup battery_threshold_for_shutdown battery_threshold_for_turnon

Remember that times need to be set in UTC.
";
        say "Current settings:";
        say `/usr/bin/python3 /home/ilce/bin/pijuice_tools/reboot.py show`;

    }
    else {
        system
"/usr/bin/python3 /home/ilce/bin/pijuice_tools/reboot.py reset $ARGV[0] $ARGV[1] $ARGV[2] $ARGV[3]";
        system
"/usr/bin/python3 /home/ilce/bin/pijuice_tools/reboot.py lowbattery $ARGV[2] $ARGV[3]";
        system "/usr/bin/python3 /home/ilce/bin/pijuice_tools/reboot.py show";
        say
"reboot.pl: If you have crontab set up, the above settings might be overridden if you run them near a crontab job execution.";
        say `date`;
    }
    exit;
}

my $wakehour   = $settings{"default_hour"};
my $wakeminute = $settings{"default_minute"};
my $padhour    = $wakehour;
my $padminute  = $wakeminute;
if ( length($padhour) < 2 )   { $padhour   = "0$padhour"; }
if ( length($padminute) < 2 ) { $padminute = "0$padminute"; }

&main();

sub main() {
    my $uptime = `cat /proc/uptime`;
    $uptime =~ s/ .*//;
    if ( $uptime < 5 * 60 || $force ) {

# We are within 5 minutes of boot. Make sure that the wakeup alam and battery is set properly.
        my $target =
"Alarm:  {'second': 0, 'minute': $wakeminute, 'hour': $wakehour, 'day': 'EVERY_DAY'}
Controlstatus:  {'alarm_wakeup_enabled': True, 'alarm_flag': True}
";
        my $alarm = `bin/utils/pijuice_util.py --get-alarm`;
        if ( $alarm ne $target ) {
            say $alarm;
            say $target;
            system(
"/usr/bin/python3 /home/ilce/bin/pijuice_tools/reboot.py reset $wakehour $wakeminute $settings{default_lowpower_shutoff} $settings{default_chargelevel_turnon}"
            );
            make_entry("reboot.pl: Setting up alarm/battery.");
        }
        else {
            say "reboot.pl: Alarm set properly.";
            make_entry("reboot.pl: Alarm set properly/battery.");
        }
    }
    my $minutes = 15;
    print "reboot.pl: Within $minutes minutes of boot?";
    if ( $uptime < $minutes * 60 || $force2 ) {
        say "Yes.";
        make_entry(
"reboot.pl: We're witin $minutes minutes of boot. Will not shut down due to low battery."
        );

# THis own't work due to the fact that we need utc.
#        print "Are we between $hour:00 and $hour:15? ";
#        if ( $hour eq $padhour ) {
#            say "Yes.";
#            if ( $uptime < 5 * 60 ) {
#                make_entry(
#"reboot.pl: Woken up just after $padhour:00; not applying low power condition until $padhour:$minutes"
#                );
#            }
#        }
#        else {
#            say "No.";
#        }
    }
    if ( $uptime > 5 * 60 || $force2 ) {
        say "No.";

      # We're outside of 15 minutes of boot, so we will now shut down if needed.
        my $lowpower =
          `/usr/bin/python3 /home/ilce/bin/pijuice_tools/reboot.py lowbattery`;
        if ( $lowpower =~ m/lowpowercondition\=(\w+)/ ) {
            say "reboot.pl: Low power condition = $1";
            if ( $1 eq "True" ) {
                make_entry("reboot.pl: Low power condition $1.");
            }
        }
        else {
            make_entry(
                "reboot.pl: ERROR - could not determine low power condition.");
        }
    }
}

sub make_entry ($text) {
    chomp( my $path = `date +'%Y-%m-%d/%H'` );
    print "$path\n";
    my $location = $home . "/logs/" . $path;
    print "$location\n";
    system( "mkdir", "-p", $location ) if !-d $location;
    my $date = `date --iso=sec`;
    open F, ">>$location/bootlog.txt";
    print F $text . "\t" . $date;
    print $text . "\t" . $date;
    close F;
}
