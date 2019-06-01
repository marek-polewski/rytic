from troposphere import Template, Tags, Output, FindInMap, Export, Join, Ref, AWS_REGION

import troposphere.ec2 as ec2


template = Template()
template.add_description('This stack sets up simple networking')


# Part 1 - creating objects

vpc = template.add_resource(
    ec2.VPC(
        'VPC',
        CidrBlock='10.0.0.0/16',
        EnableDnsSupport=True,
        EnableDnsHostnames=True,
        Tags=Tags(
            Name="OurVpc"
        )
    )
)

igw = template.add_resource(
    ec2.InternetGateway(
        'InternetGateway',
        Tags=Tags(
            Name="OurInternetGateway"
        )
    )
)

template.add_resource(
    ec2.VPCGatewayAttachment(
        'GatewayAttachment', 
        VpcId=Ref(vpc), 
        InternetGatewayId=Ref(igw)
    )
)

route_table = template.add_resource(
    ec2.RouteTable(
        'RouteTable',
        VpcId=Ref(vpc),
        Tags=Tags(
            Name="OurRouteTable"
        )
    )
)

subnets = {
    'a': '10.0.1.0/24',
    'b': '10.0.2.0/24',
    'c': '10.0.3.0/24',
}

for availability_zone in ['a', 'b', 'c']:
    name = 'OurSubnet{}'.format( availability_zone.upper())
    subnet = template.add_resource(
        ec2.Subnet(
            name,
            VpcId=Ref(vpc),
            CidrBlock=subnets[availability_zone],
            AvailabilityZone=Join("", [Ref(AWS_REGION), availability_zone]),
            MapPublicIpOnLaunch=True,
            Tags=Tags(
                Name=name,
            )
        )
    )
    template.add_resource(
        ec2.SubnetRouteTableAssociation(
            '{}2{}'.format(subnet.name, route_table.name),
            SubnetId=Ref(subnet),
            RouteTableId=Ref(route_table)
        )
    )


template.add_resource(ec2.Route(
    'DefaultRouteFront',
    GatewayId=Ref(igw),
    RouteTableId=Ref(route_table),
    DestinationCidrBlock='0.0.0.0/0'
))

justssh_security_group = template.add_resource(
    ec2.SecurityGroup(
        'JustSshSecurityGroup',
        GroupDescription='This group allow only ssh',
        VpcId=Ref(vpc),
        SecurityGroupIngress=[
            ec2.SecurityGroupRule(IpProtocol='tcp', FromPort=22, ToPort=22, CidrIp='0.0.0.0/0')
        ],
        Tags=Tags(
            Name="JustSshInput",
        )
    )
)

openbar_security_group = template.add_resource(
    ec2.SecurityGroup(
        'OpenBarSecurityGroup',
        GroupDescription='This group allow anything',
        VpcId=Ref(vpc),
        SecurityGroupIngress=[
            ec2.SecurityGroupRule(IpProtocol='tcp', FromPort=0, ToPort=65535, CidrIp='0.0.0.0/0'),
            ec2.SecurityGroupRule(IpProtocol='udp', FromPort=0, ToPort=65535, CidrIp='0.0.0.0/0')
        ],
        Tags=Tags(
            Name="OpenBar",
        )
    )
)

# Part 2 - exporting resources for other stacks 
template.add_output([
    Output(
        "NetworkVpcId",
        Description="ID of shared VPC",
        Value=Ref(vpc),
        Export=Export('network:VpcID')
    ),
    Output(
        'NetworkSubnets',
        Description='All shared subnets',
        Value=Join(',', [Ref('OurSubnetA'), Ref('OurSubnetB'), Ref('OurSubnetC')]),
        Export=Export('network:Subnets')
    ),
    Output(
        'OpenBarSG',
        Description='Security Group that allow everything',
        Value=Ref(openbar_security_group),
        Export=Export('network:sg:openbar')
    ),
    Output(
        'JustSshSG',
        Description='Security Group that allow everything',
        Value=Ref(openbar_security_group),
        Export=Export('network:sg:justssh')
    ),
])

out = './template.json'

with open(out, 'w') as f:
    f.write(template.to_json())

print('Cloudformation template saved at %s' %out)
