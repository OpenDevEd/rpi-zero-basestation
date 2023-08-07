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
my $help = "";
my $string = "";
my $number = "";
use Getopt::Long;
GetOptions (
    "string=s" => \$string,
    "help" => \$help,
    "number=f" => \$number,
    ) or die("Error in command line arguments\n");

my $last = 0;
if (-e "$0.last") {
    chomp($last = `cat $0.last`);
};

my @all = split /\n/, `python export_db.py $last`;

my %x;
foreach (@all) {
    #say "X$_";
    if (m/("sensor": "\w+"|"topic": "A\d+ .*?"|"battery_level":|"sensorbox": "\d+")/) {
	$x{$1} = $_;
    };
    if (m/^\((\d+)/) {
	$last = $1;
    };
};

open F,">$0.last";
print F $last;
close F;

open F, ">$0.data";
foreach (sort keys %x) {
    say F "$_:\n\t$x{$_}";
};
close F;
