#!/usr/bin/perl
use warnings; use strict; use utf8;
use open IO => ':encoding(UTF-8)', ':std';
use feature qw{ say signatures }; no warnings qw{ experimental::signatures };
# use experimental 'smartmatch'; use experimental qw(declared_refs);
# use 5.34.0; use experimental qw{ try }; no warnings { experimental::try };
#use File::Slurper qw(read_text read_lines write_text);
my $home = $ENV{HOME};
my $hasargs = $#ARGV;
my $help = "";
my $string = "";
my $number = "";

(my $path = $0) =~ s/\/[^\/]+$//;

chdir($path);

# #my @sensors = (
#     "aht20", 1,
#     "bh1750", 1,
#     "scd40", 0
#     );

my @sensors = ("aht20",
	       "bh1750"
    );

&main();

sub main() {
    chomp(my $location = `date +'%Y-%m-%d/%H/'`);
    chomp(my $file = `date +'sensorboard_%Y-%m-%dT%H.csv'`);
    chomp(my $time = `date --iso=seconds`);
    $location = $home . "/logs/$location";
    $file = $location . "/" . $file;
    system("mkdir","-p",$location) if !-d $location;
    say "$file";
    my %reading;
    my %header;
    my @reading;
    my @header;
    foreach my $s (@sensors) {
	my @line = split /\n/, `python $s.py`;
	$reading{$s} = $line[1];
	$header{$s} = $line[0];
	push @reading, $line[1];
	push @header, $line[0];
    };
    my $header = "date," . join ",", @header;
    my $reading = $time . "," . join ",", @reading;
    say $header;
    say $reading;
    open F, ">>$file";
    if (!-e $file) {
	say F 
    };
    say F $reading;
    close F;
};


__END__
    #use String::ShellQuote; $string = shell_quote(@list);
    #use Data::Dumper;
    #use JSON qw( decode_json  encode_json to_json from_json);
    #use Encode;
    #use Try::Tiny;
    # Path::Tiny; IO::All
    # my ($volume,$directories,$file) = File::Spec->splitpath( $path );
