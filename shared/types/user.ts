export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'developer' | 'user';
  createdAt: Date;
  updatedAt: Date;
}

export interface UserCreateRequest {
  email: string;
  name: string;
  password: string;
  role?: 'developer' | 'user';
}

export interface UserUpdateRequest {
  name?: string;
  email?: string;
}
