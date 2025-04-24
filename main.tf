provider "aws" {
  region = "us-east-1"
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "summarizer-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = true
}

module "eks" {
  source = "terraform-aws-modules/eks/aws"
  
  cluster_name    = "prod-cluster"
  cluster_version = "1.27"
  
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnets
  
  eks_managed_node_groups = {
    main = {
      min_size     = 2
      max_size     = 5
      desired_size = 3
      
      instance_types = ["t3.medium"]
    }
  }
}

module "ecr" {
  source = "terraform-aws-modules/ecr/aws"
  
  repository_name = "summarizer-api"
  
  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 30 images"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["v"]
          countType     = "imageCountMoreThan"
          countNumber   = 30
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}