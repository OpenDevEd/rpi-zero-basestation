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

&main();

sub main() {
    my $uptime = `uptime -p`;
    if ($uptime =~ m/(\d+) minutes/) {
	say "$1 minutes";
	if ($1 < 5) {
	    system("/usr/bin/python3 /home/ilce/bin/pijuice_tools/reboot.py reset");
	};
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
