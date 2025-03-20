package com.example.tinyfarm.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "farms")
public class Farm {

    @Id
    private String username; // ID = nom de l'utilisateur loggé

    private String name;
    private String location;

    // Constructeurs
    public Farm() {}

    public Farm(String username, String name, String location) {
        this.username = username;
        this.name = name;
        this.location = location;
    }

    // Getters et setters
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }
}
