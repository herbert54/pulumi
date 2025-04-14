import pulumi
import pulumi_aws as aws

# Leer configuración
config = pulumi.Config()
ami_id = config.get("ami_id") or "ami-0fc5d935ebf8bc3bc"  # Ubuntu 22.04
key_name = config.get("key_name") or "vockey"

#Grupo de seguridad
sg = aws.ec2.SecurityGroup("vm-sg",
    description="Permitir SSH y HTTP",
    ingress=[
        {"protocol": "tcp", "from_port": 22, "to_port": 22, "cidr_blocks": ["0.0.0.0/0"]},
        {"protocol": "tcp", "from_port": 80, "to_port": 80, "cidr_blocks": ["0.0.0.0/0"]},
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]},
    ]
)

#Disco de 20 GB
ebs_block = {
    "device_name": "/dev/xvda",
    "ebs": {
        "volume_size": 20,
        "delete_on_termination": True,
        "volume_type": "gp2",
    }
}

#Instancia EC2
instance = aws.ec2.Instance("vm-cloud",
    ami=ami_id,
    instance_type="t2.micro",
    key_name=key_name,
    vpc_security_group_ids=[sg.id],
    root_block_device=ebs_block,
    tags={"Name": "vm-cloud"}
)

# Outputs
pulumi.export("instance_id", instance.id)
pulumi.export("instance_ip", instance.public_ip)
