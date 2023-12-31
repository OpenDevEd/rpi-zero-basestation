#!/usr/bin/perl
use warnings; use strict; use utf8;

my $login = (getpwuid $>);
die "must run as root" if $login ne 'root';

chomp(my $remotehost = `sudo -u ilce ssh root\@157.245.35.62 "hostname"`);
if ($remotehost eq "ssh-tunnel-exchange-point") {
} else {    
    print("$remotehost This will only work if you have the ssh keys exchanged properly. Check your keys.");
    exit;
};

if (!-e "/usr/bin/autossh") {
    system("sudo apt install autossh");
} else {
    print "autossh installed.\n";
};

my $text = `cat install-autossh.service.txt`;

chomp(my $host = `hostname`);

if ($host =~ m/(\d+)/) {
    my $number = $1;
    while (length($number) < 3) {
	$number = "0$number";
    };
    $number = "22$number";
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
