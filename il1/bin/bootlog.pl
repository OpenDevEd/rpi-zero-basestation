#!/usr/bin/perl
my $home = $ENV{HOME};

my $pause = 60;
make_entry("boot");
sleep $pause;
make_entry("boot + $pause seconds");

sub make_entry() {
    chomp(my $path = `date +'%Y-%m-%d/%H'`);
    print "$path\n";
    my $location = $home . "/logs/" . $path;
    print "$location\n";
    system("mkdir","-p",$location) if !-d $location;
    my $date = `date --iso=sec`;
    open F,">>$location/bootlog.txt";
    print F $_[0] . "\t" . $date;
    print $_[0] . "\t" . $date;
    close F;
};



