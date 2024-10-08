// Define the Job and Certificate types
interface JobType {
  id: number;
  title: string;
  description: string;
  responsibilities: string;
  prerequisites: { id: string; name: string }[];
}

interface CertificateType {
  id: string;
  name: string;
}
