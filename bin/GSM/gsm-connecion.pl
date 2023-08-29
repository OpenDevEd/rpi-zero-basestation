#!/usr/bin/perl
use warnings; use strict; use utf8;
use open IO => ':encoding(UTF-8)', ':std';
use feature qw{ say signatures }; no warnings qw{ experimental::signatures };
# use experimental 'smartmatch'; use experimental qw(declared_refs);
# use 5.34.0; use experimental qw{ try }; no warnings { experimental::try };
# use File::Slurper qw(read_text read_lines write_text);
my $home = $ENV{HOME};
chomp(my $date = `date +'%Y-%m-%d_%H.%M.%S'`);
chomp(my $iso = `date --iso=seconds`);
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

if ($hasargs == -1 || $help) {
    print("Need arguments");
    print "Sorry, no help.";
    system("less","$0");
    exit;
};

if ($ARGV[0] eq "on") {
       chdir("$home/rpi-zero-basestation/bin/GSM/");
       system("./phat-gsm_on_off.py on");
       $|=1;
       for (my $i=1; $i<=10; $i++) {
	   print ".";
	   sleep 1;
       };
       say "";
       open L,"tail -n 0 -f /var/log/messages|";
       system("sudo pon gsm.mm");
       my $status = "";
       while (<L>) {
	   print;
	   if (m/(chat\[\d+\]\: Failed|pppd\[\d+\]: Exit.|secondary DNS address)/) {
	       $status = $_;
	       if ($1 eq "secondary DNS address") {
		   $status = "success";
	       };
	       last;
	   };
       };
       close L;
       say "Status: $status";
} elsif ($ARGV[0] eq "off") {
    system("sudo poff gsm.mm");
    system("./phat-gsm_on_off.py off");
} elsif ($ARGV[0] eq "test") {
    say "Testing ping, please wait";
    system "ping -c 3 -I ppp0 -n google.com";
    say "Testing https - must be run with sudo, please wait";
    system "sudo curl -v -4 --interface ppp0 https://google.com";
} else {
    say "Valid options: on off ip test";
};
