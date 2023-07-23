#!/usr/bin/perl
use warnings; use strict; use utf8;
use open IO => ':encoding(UTF-8)', ':std';
use feature qw{ say signatures }; no warnings qw{ experimental::signatures };
# use experimental 'smartmatch'; use experimental qw(declared_refs);
# use 5.34.0; use experimental qw{ try }; no warnings { experimental::try };
#use File::Slurper qw(read_text read_lines write_text);
my $home = $ENV{HOME};
chomp(my $date = `date +'%Y-%m-%d_%H.%M.%S'`);
chomp(my $hour = `date +'%H'`);
chomp(my $minute = `date +'%M'`);
my $hasargs = $#ARGV;
my $help = "";
my $string = "";
my $number = "";
use Getopt::Long;
GetOptions (
    "string=s" => \$string, 
    "help" => \$help, 
    "number=f" => \$number, 
    ) or die("Error in command line arguments\n");

&main();

sub main() {
    my $uptime = `cat /proc/uptime`;
    $uptime =~ s/ .*//;    
    if ($uptime < 5 * 60) {
	my $target = "Alarm:  {'second': 0, 'minute': 0, 'hour': 6, 'day': 'EVERY_DAY'}
Controlstatus:  {'alarm_wakeup_enabled': True, 'alarm_flag': True}
";
	my $alarm = `bin/utils/pijuice_util.py --get-alarm`;
	if ($alarm ne $target) {
	    say $alarm;
	    say $target;
	    system("/usr/bin/python3 /home/ilce/bin/pijuice_tools/reboot.py reset");
	} else {
	    say "Alarm set properly.";
	};
    };
    if ($uptime < 60 * 60 && $hour eq "06") {
	say "Booted and after 6:00? Yes.";
    } else {
	say "Booted and after 6:00? No.";
    };
};
 
__END__
    #use String::ShellQuote; $string = shell_quote(@list);
    #use Data::Dumper;
    #use JSON qw( decode_json  encode_json to_json from_json);
    #use Encode;
    #use Try::Tiny;
    # Path::Tiny; IO::All
    # my ($volume,$directories,$file) = File::Spec->splitpath( $path );
