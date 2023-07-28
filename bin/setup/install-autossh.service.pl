#!/usr/bin/perl
use warnings; use strict; use utf8;
use File::Slurper qw(read_text read_lines write_text);

print("Run with sudo\n");
system("sudo apt install autossh");
my $text = read_text("autossh.service");

chomp(my $host = `hostname`);

if ($host =~ m/(\d+)/) {
    my $number = $1;
    while (length($number) < 3) {
	$number = "0$nunber";
    };
    $number = "22$nunber";
    $text =~ s/\<PORT\>/$number/s;

    print "Setting up autossh service connecting to port $number\n";
    open F,">/etc/systemd/system/autossh.service";
    print F $text;
    close F;
    
    system("sudo systemctl enable autossh.service");
    system("sudo systemctl start autossh.service");
} else {
    print "Could not determine host number from $host.";
};
