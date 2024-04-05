qemu-nbd --connect=/dev/nbd0 /var/lib/libvirt/images/ZealOS-2.qcow2
mkdir -p /tmp/zealos
mount /dev/nbd0p1 /tmp/zealos/
cp chal.bin /tmp/zealos/Home/chal.GR32
umount /dev/nbd0p1
qemu-nbd --disconnect /dev/nbd0
