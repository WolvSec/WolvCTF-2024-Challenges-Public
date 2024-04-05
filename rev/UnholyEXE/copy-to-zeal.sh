qemu-nbd --connect=/dev/nbd0 /var/lib/libvirt/images/ZealOS-2.qcow2
mkdir -p /tmp/zealos
mount /dev/nbd0p1 /tmp/zealos/
cp chal.ZC /tmp/zealos/Home/
cp chal.PRJ /tmp/zealos/Home/
cp /tmp/zealos/Home/chal.ZXE chal.bin
cp Sockets.HH /tmp/zealos/Home/
cp BST.HH /tmp/zealos/Home/
umount /dev/nbd0p1
qemu-nbd --disconnect /dev/nbd0
