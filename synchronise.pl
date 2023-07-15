#!/usr/bin/perl
use warnings; use strict; use utf8;
use open IO => ':encoding(UTF-8)', ':std';
use feature qw{ say signatures }; no warnings qw{ experimental::signatures };
# use experimental 'smartmatch'; use experimental qw(declared_refs);
# use 5.34.0; use experimental qw{ try }; no warnings { experimental::try };
#use File::Slurper qw(read_text read_lines write_text);
my $home = $ENV{HOME};
chomp(my $date = `date +'%Y-%m-%d_%H.%M.%S'`);
my $hasargs = $#ARGV;
my $update = "";
my $retrieve = "";
use Getopt::Long;
my $help = "";
GetOptions (
    "update" => \$update, 
    "retrieve" => \$retrieve, 
    "help" => \$help,
    ) or die("Error in command line arguments\n");

if ($hasargs == -1 || $help) {
    say "

Update instances at ssh il1 and il2:

synchronise --update il1 il2


Copy back data from il1

synchronise --retrieve il1

";
    exit;
};

&main();

sub main() {
    foreach my $server (@ARGV) {
	if ($retrieve) {
	    system("rsync","-avz",$server. ":bin", ".");
	};
	if ($update) {
	    system("rsync","-avz","bin",$server);
	};
    };
};

